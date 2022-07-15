import asyncio
import logging
from typing import Tuple
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async, async_to_sync
from player_lookup.models import Player
from player_lookup.views import (
    create_matches_from_battlelog,
    get_player_battlelog,
    get_player_data,
    create_or_update_club,
)

logger = logging.getLogger("django")

class Command(BaseCommand):
    help = "Update every player in the database"

    def handle(self, *args, **options):
        logger.info("Starting update_all_players, fetching all players from DB...")
        all_players = Player.objects.all()
        logger.info(f"Found {len(all_players)} players in DB.")
        logger.info("Fetching all players profiles and battlelogs from API...")
        tag_battlelog, tag_clubtag = \
            self.get_all_players_profiles_and_battlelog(all_players)
        logger.info("Creating matches from battlelog ...")
        for tag, battlelog in tag_battlelog.items():
            create_matches_from_battlelog(tag, battlelog)
        logger.info("Updating players clubs...")
        for tag, club_tag in tag_clubtag.items():
            self.update_player_club({tag: club_tag})

        logger.info("Updating players' brawlclub rating...")
        for player in all_players:
            player.update_brawlclub_rating()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all players"), ending="\n"
        )

    @async_to_sync
    async def get_all_players_profiles_and_battlelog(self, players) -> Tuple[dict, dict]:
        """Get all players profiles and battlelogs.

        Keyword arguments:
        players -- List of players tags

        Returns
        Tuple with :
        Dict matching player tag and battle log
        Dict matching player tag and club tag
        """
        players = await sync_to_async(list)(Player.objects.all())
        api_calls = []
        for player in players:
            response = get_player_data(player.player_tag)
            api_calls.append(response)
        responses = await asyncio.gather(*api_calls)
        results = {"Player data": responses}
        tag_profile = {}
        for player in results["Player data"]:
            try:
                tag_profile[player["tag"]] = player
            except KeyError:
                logger.info("request throttled, skipping")
                continue
        api_calls = []
        tag_clubtag = {}
        for tag, profile in tag_profile.items():
            if profile["club"]:
                club_tag = profile["club"]["tag"]
                tag_clubtag[tag] = club_tag
            response = get_player_battlelog(tag)
            api_calls.append(response)
        battlelogs = await asyncio.gather(*api_calls)
        tag_battlelog = {}
        for tag, battlelog in zip(tag_profile.keys(), battlelogs):
            tag_battlelog[tag] = battlelog

        return tag_battlelog, tag_clubtag

    def update_player_club(self, tag_clubtag: dict) -> None:
        """Update player's club.

        Keyword arguments:
        tag_clubtag -- Dict matching player tag and club tag
        """
        players_to_update = []
        for tag, clubtag in tag_clubtag.items():
            player = Player.objects.get(player_tag=tag)
            if clubtag is None:
                player.club = None
                players_to_update.append(player)
            elif player.club and player.club.club_tag == clubtag:
                continue
            else:
                club = create_or_update_club(clubtag)
                player.club = club
                players_to_update.append(player)


        Player.objects.bulk_update(players_to_update, ["club"])