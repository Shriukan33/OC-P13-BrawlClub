import asyncio
import logging
from datetime import datetime
from typing import Tuple

import dateutil.parser
from django.shortcuts import get_object_or_404
import httpx
from asgiref.sync import async_to_sync, sync_to_async
from django.db.models import Avg, Count
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response

from . import models, serializers
from .brawlstars_api import BrawlAPi

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
            queryset = None
        return queryset


class SingleEntityView(RetrieveAPIView):
    """
    Return a single entity (Club or player).
    """

    # The original tag in url kwargs misses the "#"
    # so we need to add it back in here.
    lookup_url_kwarg = "proper_tag"

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
            queryset = None
        return queryset


class SearchUnknownEntityView(RetrieveAPIView):
    """Returns either a Player or a Club instance based on a provided tag"""

    queryset = models.Player.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        """
        Return the context-appropriate object.
        """
        tag = self.kwargs.get("tag", None)
        if tag:
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
            "snapshot_date")[:8]

        return queryset

@async_to_sync
async def get_club_members_data(request, club_tag) -> dict:
    """Get the profile page and battlelog of every member of a given club"""
    member_list = await brawl_api.get_club_members_tag_list(club_tag)
    # We prepare the api calls in a list so we're able to await them all
    api_calls = []
    async with httpx.AsyncClient(timeout=3600) as client:
        for member in member_list:
            response = get_player_data(member, client)
            api_calls.append(response)

        # We await all the api calls
        responses = await asyncio.gather(*api_calls)
    # The respons is a list of all players profile from the given clan
    results = {"Player data": responses}
    # tag_profile = {player["tag"]: player for player in results["Player data"]}

    tag_profile = {}
    for player in results["Player data"]:
        tag = player.get("tag", None)
        if not tag:
            continue
        tag_profile[tag] = player

    # We now get the battlelog of each player usig the tags we retrieved
    api_calls = []
    async with httpx.AsyncClient(timeout=3600) as client:
        for tag, _ in tag_profile.items():
            response = get_player_battlelog(tag, client)
            api_calls.append(response)

        battlelogs = await asyncio.gather(*api_calls)

    # Now we match the battlelogs with the player tags
    tag_battlelog = {}
    for tag, battlelog in zip(tag_profile.keys(), battlelogs):
        tag_battlelog[tag] = battlelog

    return tag_profile, tag_battlelog


async def get_player_data(player_tag: str, client: httpx.AsyncClient) -> dict:
    """Return player's profile data given a player tag"""
    url = brawl_api.get_player_stats_url(player_tag)
    response = await client.get(url, headers=brawl_api.headers)
    return response.json()


# Entry point
def update_club_members(request, club_tag: str) -> JsonResponse:
    """Test async to sync"""
    tag_profile, tag_battlelogs = get_club_members_data(request, club_tag)
    club = create_or_update_club(club_tag)
    player_ids = models.Player.objects.values_list("player_tag", flat=True)
    players_to_update = []
    players_to_create = []
    for _, profile in tag_profile.items():
        player_instance = create_player_instance(profile, club)
        if player_instance.player_tag in player_ids:
            players_to_update.append(player_instance)
        else:
            players_to_create.append(player_instance)

    models.Player.objects.bulk_create(players_to_create)
    models.Player.objects.bulk_update(players_to_update, ["trophy_count", "club"], 999)

    for tag, battlelog in tag_battlelogs.items():
        create_matches_from_battlelog(tag, battlelog)

    return JsonResponse(tag_battlelogs, safe=False)


def update_all_clubs(request):
    """Update all clubs"""
    clubs = models.Club.objects.all().iterator()
    for club in clubs:
        update_club_members({}, club.club_tag)

    return HttpResponse("Updated all clubs")


def create_or_update_club(club_tag: str) -> models.Club:
    """Create  or udpate a club"""
    if not club_tag:
        return None
    club_information = brawl_api.get_club_information(club_tag)
    defaults = {
        "club_name": club_information["name"],
        "club_description": club_information.get("description", ""),
        "club_type": club_information["type"],
        "club_tag": club_information["tag"],
        "trophies": club_information["trophies"],
        "required_trophies": club_information["requiredTrophies"],
    }
    club, created = models.Club.objects.update_or_create(
        club_tag=club_information["tag"], defaults=defaults
    )

    if created:
        logger.info(f"Created club {club.club_name}")
    else:
        logger.info(f"Updated club {club.club_name}")

    return club


def create_player_instance(player: dict, club: models.Club) -> models.Player:
    """Create a player instance.

    Keyword arguments:
    - player -- the player's profile
    - club -- the club the player belongs to

    Returns:
    - the player instance
    """

    defaults = {
        "player_tag": player["tag"],
        "player_name": player["name"],
        "trophy_count": player["trophies"],
        "club": club,
    }
    player_instance = models.Player(**defaults)

    return player_instance


async def get_player_battlelog(player_tag: str, client: httpx.AsyncClient) -> dict:
    """Return player's battlelog given a player tag."""
    url = brawl_api.get_player_battlelog_url(player_tag)
    response = await client.get(url, headers=brawl_api.headers)
    return response.json()


def create_matches_from_battlelog(player_tag: str, battlelog: dict) -> None:
    """
    Create matches from a given battlelog.

    Keyword arguments:
    - player_tag -- the player's tag
    - battlelog -- the battlelog of the player, including its 24 last matches
    """

    def get_battle_data(
        player_tag, battle: dict
    ) -> Tuple[list, list, str, str, str, datetime, bool, int, str, str]:
        """Return data from a battle.

        Keyword arguments:
        - player_tag -- the player's tag
        - battle -- the battle to get the data from

        Returns:
        A tuple with the following data:
        - a list of player tags
        - a list of player names
        - a string indicating the outcome of the match
        - a string with the played map's name
        - a string with the played mode's name
        - a datetime with the match's date
        - a bool indicating if the player is Star Player (=MVP)
        - an int indicating the number of trophies the player won
        - a string with the star player's tag (without #)
        - a string with the name of the brawler that the player used.
        """
        player_list = []
        winning_team = None
        match_outcome = None
        map_played = None
        mode = None
        is_star_player = None
        battle_date = None
        trophies_won = None
        star_players_tag = None
        played_brawler = None
        # We are only interested in Team ranked matches
        if battle.get("battle", {}).get("type", None) == "teamRanked" and battle.get(
            "battle", {}
        ).get("trophyChange", None):
            # Now we examinate each of the two teams to get the winning one
            for team_number, team in enumerate(battle["battle"]["teams"]):
                for player in team:
                    if player["tag"] == player_tag:
                        if battle["battle"]["result"] == "victory":
                            winning_team = team
                        elif battle["battle"]["result"] == "defeat":
                            # There are only two teams : 0 and 1
                            winning_team = battle["battle"]["teams"][1 - team_number]
                        elif battle["battle"]["result"] == "draw":
                            winning_team = None
                    # We add to the player list the player tags
                    player_list.append((player["tag"], player["brawler"]["name"]))

            winning_team = [
                (player["tag"], player["brawler"]["name"]) for player in winning_team
            ]
            map_played = battle["event"].get("map", None)
            mode = battle["event"].get("mode", None)
            battle_date = dateutil.parser.parse(battle["battleTime"])
            match_outcome = battle["battle"].get("result", None)
            # In the model, we store the outcome as WIN, LOSS or DRAW
            if match_outcome == "victory":
                match_outcome = "WIN"
            elif match_outcome == "defeat":
                match_outcome = "LOSS"
            elif match_outcome == "draw":
                match_outcome = "DRAW"
            else:
                match_outcome = "UNKNOWN"
            is_star_player = player_tag in battle["battle"].get("starPlayer", {}).get(
                "tag", ""
            )
            trophies_won = battle["battle"].get("trophyChange")
            star_players_tag = (
                battle["battle"].get("starPlayer", {}).get("tag", "")[1:]
            )  # We remove the #
            for tag, brawler in player_list:
                if tag == player_tag:
                    played_brawler = brawler
                    break

        return (
            player_list,
            winning_team,
            match_outcome,
            map_played,
            mode,
            battle_date,
            is_star_player,
            trophies_won,
            star_players_tag,
            played_brawler,
        )

    def get_match_type(match_outcome: str) -> Tuple[bool, bool]:
        """Return the match type.

        Keyword arguments:
        - match_outcome -- the outcome of the match (Victory, Defeat, Draw)

        Returns:
        A tuple containing two booleans to indicate if the player played a
        power match or not and if they played with a clubmate or not.
        """
        played_with_team = False
        is_power_match = False
        if match_outcome == "WIN":
            if trophies_won == 9:
                played_with_team = True
                is_power_match = True
            elif trophies_won == 4:
                played_with_team = True
        elif match_outcome == "LOSS":
            if trophies_won == 5:
                played_with_team = True
                is_power_match = True
            elif trophies_won == 2:
                played_with_team = True
        # Can't draw in Power matches
        elif match_outcome == "DRAW" and trophies_won == 3:
            played_with_team = True

        return (is_power_match, played_with_team)

    match_batch = []
    incomplete_match_issue_list = []
    match_issues_with_pre_existing_match_batch = []
    match_issues_batch = []
    if battlelog.get("reason", None) == "notFound":
        # Happens sometimes that the player's battlelog can't be found
        # It's not specific to this app
        logger.info(player_tag + ": Battlelog not found")
        return
    for battle in battlelog["items"]:
        (
            player_list,
            winning_team,
            match_outcome,
            map_played,
            mode,
            battle_date,
            is_star_player,
            trophies_won,
            star_players_tag,
            brawler_used,
        ) = get_battle_data(player_tag, battle)
        match_already_exists = False
        if player_list:
            # We don't want to create a match if it already exists
            match_id = f"{star_players_tag}{battle_date.strftime('%s')}"
            played_with_team, is_power_match = get_match_type(match_outcome)
            try:
                the_match = models.Match.objects.get(match_id=match_id)
                match_already_exists = True
            except models.Match.DoesNotExist:
                # We create a match instance but don't save it yet
                battle_type = "Power Match" if is_power_match else "Normal Match"
                the_map = models.BrawlMap.objects.get_or_create(
                    name=map_played, defaults={"name": map_played}
                )[0]
                the_match = models.Match(
                    match_id=match_id,
                    mode=mode,
                    map_played=the_map,
                    battle_type=battle_type,
                    date=battle_date,
                )
                match_batch.append(the_match)

            # We now create the associated MatchIssue
            player = models.Player.objects.get(player_tag=player_tag)

            if match_already_exists:
                # We check if the match already has an issue with the player
                match_issue_exists = models.MatchIssue.objects.filter(
                    match=the_match, player=player
                ).exists()
                if match_issue_exists:
                    continue

            brawler = models.Brawler.objects.get_or_create(
                name=brawler_used, defaults={"name": brawler_used}
            )[0]
            # MatchIssue has a FK to Match, which might not be created yet.
            # We're going to add it once the Match is created
            the_match_issue = models.MatchIssue(
                player=player,
                brawler=brawler,
                outcome=match_outcome,
                trophies_won=trophies_won,
                is_star_player=is_star_player,
                played_with_clubmate=played_with_team,
            )
            if not match_already_exists:
                incomplete_match_issue_list.append(the_match_issue)
            else:
                the_match_issue.match = the_match
                match_issues_with_pre_existing_match_batch.append(the_match_issue)

    created_matches = models.Match.objects.bulk_create(match_batch)
    for match, incomplete_match_issue in zip(
        created_matches, incomplete_match_issue_list
    ):
        incomplete_match_issue.match = match
        match_issues_batch.append(incomplete_match_issue)

    models.MatchIssue.objects.bulk_create(match_issues_batch)
    models.MatchIssue.objects.bulk_create(match_issues_with_pre_existing_match_batch)


async def update_player_profile(request, player_tag: str):
    """
    Update on demand the profile of a single player.

    Keyword arguments:
    - player_tag -- the tag of the player to update
    """
    if not player_tag.startswith("#"):
        player_tag = "#" + player_tag
    async with httpx.AsyncClient as client:
        response = get_player_data(player_tag, client)
        player_profile = await asyncio.gather(response)
        player_profile = player_profile[0]
        response = get_player_battlelog(player_tag, client)
        battlelog = await asyncio.gather(response)

    player_club_tag = player_profile.get("club", {}).get("tag", None)

    club = await sync_to_async(create_or_update_club)(player_club_tag)
    player, _ = await sync_to_async(models.Player.objects.get_or_create)(
        player_tag=player_tag,
        defaults={
            "player_tag": player_tag,
            "player_name": player_profile["name"],
            "trophy_count": player_profile["trophies"],
            "club": club,
        },
    )
    player.club = club
    await sync_to_async(player.save)()

    await sync_to_async(create_matches_from_battlelog)(player_tag, battlelog[0])

    return HttpResponse(status=200)


def get_top_clubs(size: int = 10, start: int = 0):
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


def get_top_players(size: int = 10, start: int = 0):
    """
    Get the top players in the database, ranked by their Brawlclub Rating
    """
    top = models.Player.objects.order_by(
        "-brawlclub_rating", "-total_club_war_trophy_count", "-trophy_count"
    )[start:size]
    return top
