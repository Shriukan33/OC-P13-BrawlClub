from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
import httpx
import logging
import asyncio
from asgiref.sync import async_to_sync

from .forms import PlayerLookupForm
from .brawlstars_api import BrawlAPi
from . import models

brawl_api = BrawlAPi()

logger = logging.getLogger("django")


class PlayerLookupView(FormView):
    template_name = 'player_lookup/player_lookup.html'
    form_class = PlayerLookupForm
    success_url = 'player_lookup:player_page'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        player_tag = form.cleaned_data['player_tag']
        return HttpResponseRedirect(self.get_success_url(player_tag))

    def get_success_url(self, player_tag) -> str:
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. "
                                       "Provide a success_url.")
        success_url = reverse_lazy(self.success_url, args=[player_tag])
        return success_url


class PlayerPageView(TemplateView):
    template_name = 'player_lookup/player_page.html'

    def get_context_data(self, **kwargs):
        """Displays the stats of the player."""
        player_tag = kwargs['player_tag']
        player_data = self.get_number_of_trophies_in_club_war(player_tag)
        context = super().get_context_data(**kwargs)
        context['player_data'] = player_data
        return context

    def get_number_of_trophies_in_club_war(self, player_tag: str) -> int:
        """Returns the number of trophies in club war if any in
        the last 24 matches."""
        player_battlelog = brawl_api.get_player_battlelog(player_tag)
        number_of_trophies = 0
        for match in player_battlelog['items']:
            if match['battle']['type'] == 'teamRanked':
                number_of_trophies += match["battle"].get("trophyChange", 0)
        return number_of_trophies


@async_to_sync
async def get_club_members_data(request, club_tag) -> dict:
    """Get the profile page and battlelog of every member of a given club"""
    member_list = brawl_api.get_club_members_tag_list(club_tag)
    # We prepare the api calls in a list so we're able to await them all
    api_calls = []
    for member in member_list:
        response = get_player_data(member)
        api_calls.append(response)

    # We await all the api calls
    responses = await asyncio.gather(*api_calls)
    # The respons is a list of all players profile from the given clan
    results = {"Player data": responses}
    tag_profile = {player["tag"]: player for player in results["Player data"]}

    # We now get the battlelog of each player usig the tags we retrieved
    api_calls = []
    for tag, _ in tag_profile.items():
        response = get_player_battlelog(tag)
        api_calls.append(response)

    battlelogs = await asyncio.gather(*api_calls)

    # Now we match the battlelogs with the player tags
    tag_battlelog = {}
    for tag, battlelog in zip(tag_profile.keys(), battlelogs):
        tag_battlelog[tag] = battlelog

    return tag_profile, tag_battlelog


async def get_player_data(player_tag: str) -> dict:
    """Return player's profile data given a player tag"""
    async with httpx.AsyncClient() as client:
        url = brawl_api.get_player_stats_url(player_tag)
        response = await client.get(url, headers=brawl_api.headers)
        return response.json()


def update_club_members(request, club_tag: str) -> JsonResponse:
    """Test async to sync"""
    tag_profile, tag_battlelogs = get_club_members_data(request, club_tag)
    club = create_or_update_club(club_tag)
    for _, value in tag_profile.items():
        create_or_update_player(value, club)
    return JsonResponse(tag_battlelogs, safe=False)


def create_or_update_club(club_tag: str) -> models.Club:
    """Create  or udpate a club"""
    if not club_tag:
        return None
    club_information = brawl_api.get_club_information(club_tag)
    defaults = {
        "club_name": club_information['name'],
        "club_description": club_information['description'],
        "club_type": club_information['type'],
        "club_tag": club_information['tag'],
        "trophies": club_information['trophies'],
        "required_trophies": club_information['requiredTrophies']
    }
    club, created = models.Club.objects.update_or_create(
        club_tag=club_information['tag'],
        defaults=defaults)

    if created:
        logger.info(f"Created club {club.club_name}")
    else:
        logger.info(f"Updated club {club.club_name}")

    return club


def create_or_update_player(player: dict, club: models.Club) -> models.Player:
    """Create or update a player"""

    if not club:
        club_tag = player["club"].get("tag", None)
        if club_tag:
            club = create_or_update_club(club_tag)
        else:
            club = None

    defaults = {
        "player_tag": player['tag'],
        "player_name": player['name'],
        "trophy_count": player['trophies'],
        "club": club,
    }
    player, created = models.Player.objects.update_or_create(
        player_tag=player['tag'],
        defaults=defaults)

    if created:
        logger.info(f"Created player {player.player_name}")
    else:
        logger.info(f"Updated player {player.player_name}")

    return player


async def get_player_battlelog(player_tag: str) -> dict:
    """Return player's battlelog given a player tag"""
    async with httpx.AsyncClient() as client:
        url = brawl_api.get_player_battlelog_url(player_tag)
        response = await client.get(url, headers=brawl_api.headers)
        return response.json()

