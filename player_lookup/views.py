import logging
from typing import TYPE_CHECKING, Union

from asgiref.sync import async_to_sync, sync_to_async
from django.db.models import Avg, Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import models, serializers
from .brawlstars_api import BrawlAPi
from .update_services import update_club_members, update_player_profile

if TYPE_CHECKING:  # pragma: no cover
    from django.db.models.query import QuerySet
    from player_lookup.models import Club, Player

brawl_api = BrawlAPi()

logger = logging.getLogger("django")


class LeaderBoardView(ListAPIView):
    """
    Return the top entities (Club or players).
    """

    class LeaderBoardPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = "page_size"
        max_page_size = 100

    pagination_class = LeaderBoardPagination

    @method_decorator(cache_page(60 * 60 * 12))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return the context-appropriate queryset.
        """
        entity = self.kwargs.get("entity", None)
        if entity == "players":
            queryset = models.Player.objects.order_by(
                "-brawlclub_rating", "-total_club_war_trophy_count", "-trophy_count"
            )
            self.serializer_class = serializers.PlayerSerializer

        elif entity == "clubs":
            queryset = (
                models.Club.objects.annotate(avg_bcr=Avg("player__brawlclub_rating"))
                .annotate(nb_of_players=Count("player"))
                .order_by("-avg_bcr", "-trophies")
                .filter(nb_of_players__gte=25)
            )
            self.serializer_class = serializers.ClubSerializer
        else:
            logger.info(f"Invalid entity type: {entity}")
            raise Http404
        return queryset


class SingleEntityView(RetrieveAPIView):
    """
    Return a single entity (Club or player).
    """

    # The original tag in url kwargs misses the "#"
    # so we need to add it back in here.
    lookup_url_kwarg = "proper_tag"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if not instance.has_been_searched:
            instance: Union["Player", "Club"]
            instance.has_been_searched = True
            instance.save()
        return Response(serializer.data)

    def get_queryset(self):
        """
        Return the context-appropriate queryset.
        """
        entity = self.kwargs.get("entity", None)
        tag = self.kwargs.get("tag", None)
        if tag:
            self.kwargs.update({"proper_tag": "#" + tag})
        if entity == "player":
            queryset = models.Player.objects.all()
            self.lookup_field = "player_tag"
            self.serializer_class = serializers.PlayerSerializer
        elif entity == "club":
            queryset = models.Club.objects.all()
            self.lookup_field = "club_tag"
            self.serializer_class = serializers.ClubSerializer
        else:
            logger.info(f"Invalid entity type: {entity}")
            raise Http404
        return queryset


class SearchUnknownEntityView(RetrieveAPIView):
    """Returns either a Player or a Club instance based on a provided tag"""

    queryset = models.Player.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            self.fetch_entity(request, *args, **kwargs)
            instance = self.get_object()
            if isinstance(instance, models.Player):
                if instance.club:
                    update_club_members(instance.club.club_tag)

        if instance:
            instance: Union["Player", "Club"]
            if not instance.has_been_searched:
                instance.has_been_searched = True
                instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @async_to_sync
    async def fetch_entity(
        self, request, *args, **kwargs
    ) -> Union[models.Player, models.Club, None]:
        entity_type = brawl_api.is_player_or_club(kwargs["tag"])
        if entity_type == "player":
            self.serializer_class = serializers.PlayerSerializer
            await update_player_profile(kwargs["tag"])

        elif entity_type == "club":
            self.serializer_class = serializers.ClubSerializer
            await sync_to_async(update_club_members)(kwargs["tag"])

    def get_object(self):
        """
        Return the context-appropriate object.
        """
        tag = self.kwargs.get("tag", None)
        if tag:
            if not tag.startswith("#"):
                tag = "#" + tag
        try:
            obj = self.queryset.get(player_tag=tag)
            self.serializer_class = serializers.PlayerSerializer
        except models.Player.DoesNotExist:
            try:
                obj = models.Club.objects.get(club_tag=tag)
                self.serializer_class = serializers.ClubSerializer
            except models.Club.DoesNotExist:
                obj = None
        return obj


class ClubMembersView(ListAPIView):
    """
    Return the members of a club.
    """

    lookup_url_kwarg = "club_tag"

    def get_queryset(self):
        """
        Return the context-appropriate queryset.
        """
        club_tag = self.kwargs.get("club_tag", None)
        if club_tag:
            if not club_tag.startswith("#"):
                self.kwargs.update({"club_tag": "#" + club_tag})
        queryset = models.Player.objects.filter(club__club_tag=club_tag).order_by(
            "-brawlclub_rating"
        )
        self.serializer_class = serializers.PlayerSerializer
        return queryset


class ClubFinderResultsView(ListAPIView):
    """
    Return the clubs that match the search query.
    """

    serializer_class = serializers.ClubSerializer

    def get_queryset(self):
        """
        Return the context-appropriate queryset.
        """
        max_trophies = self.request.GET.get("max_trophies", None)
        types_list = self.request.GET.get("type", None)
        min_members = self.request.GET.get("min_members", None)
        max_members = self.request.GET.get("max_members", None)
        queryset = (
            models.Club.objects.annotate(avg_bcr=Avg("player__brawlclub_rating"))
            .annotate(nb_of_players=Count("player"))
            .order_by("-avg_bcr", "-trophies")
        )
        if types_list:
            try:
                types_list = types_list.split(",")
                for type in types_list:
                    if type not in ["open", "inviteOnly", "closed"]:
                        raise ValueError
                queryset = queryset.filter(club_type__in=types_list)
            except ValueError:
                logger.info(f"Invalid types list: {types_list}")
        if max_trophies:
            try:
                max_trophies = int(max_trophies)
                queryset = queryset.filter(required_trophies__lte=max_trophies)
            except ValueError:
                logger.info(f"Invalid max_trophies value: {max_trophies}")
        if min_members:
            try:
                min_members = int(min_members)
                queryset = queryset.filter(nb_of_players__gte=min_members)
            except ValueError:
                logger.info(f"Invalid min_members value: {min_members}")
        if max_members:
            try:
                max_members = int(max_members)
                queryset = queryset.filter(nb_of_players__lte=max_members)
            except ValueError:
                logger.info(f"Invalid max_members value: {max_members}")

        return queryset.order_by("-avg_bcr", "-trophies")[:25]


class PlayerAreaGraphView(ListAPIView):
    """
    Return the area graph data for a player.
    """

    serializer_class = serializers.PlayerHistorySerializer

    def get_queryset(self):
        """
        Return the context-appropriate queryset.
        """
        tag = self.kwargs.get("player_tag", None)
        if tag:
            if not tag.startswith("#"):
                self.kwargs.update({"player_tag": "#" + tag})
                tag = "#" + tag
        player = get_object_or_404(models.Player, player_tag=tag)
        queryset = models.PlayerHistory.objects.filter(player=player).order_by(
            "snapshot_date"
        )[:8]

        return queryset


def get_top_clubs(size: int = 10, start: int = 0) -> "QuerySet[Club]":
    """
    Get the top clubs in the database, ranked by the average
    BrawlClub Rating of its players
    """
    top = (
        models.Club.objects.annotate(avg_bcr=Avg("player__brawlclub_rating"))
        .annotate(nb_of_players=Count("player"))
        .order_by("-avg_bcr", "-trophies")
        .filter(nb_of_players__gte=25)[start:size]
    )
    return top


def get_top_players(size: int = 10, start: int = 0) -> "QuerySet[Player]":
    """
    Get the top players in the database, ranked by their Brawlclub Rating
    """
    top = models.Player.objects.order_by(
        "-brawlclub_rating", "-total_club_war_trophy_count", "-trophy_count"
    )[start:size]
    return top
