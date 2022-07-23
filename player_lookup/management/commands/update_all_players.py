import asyncio
from datetime import datetime, timedelta, timezone
import logging
import httpx
from typing import Tuple
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async, async_to_sync
from player_lookup.models import Club, Player
from player_lookup.views import (
    create_matches_from_battlelog,
    get_player_battlelog,
    get_player_data,
    brawl_api,
)

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Update every player in the database"

    def handle(self, *args, **options):
        logger.info("Starting update_all_players command...")
        min_time_since_last_update = datetime.now(timezone.utc) - timedelta(minutes=30)
        total_player_count = Player.objects.count()
        player_count = Player.objects.filter(last_updated__lte=min_time_since_last_update).count()
        logger.info(f"Found {player_count} players to update in DB (Total : {total_player_count})")
        batch_size = 500
        top_limit = player_count // batch_size * batch_size
        first_loop = True
        for i in range(0, top_limit + 1, batch_size):
            if first_loop:
                first_loop = False
                new_start = i
                continue

            logger.info(f"Updating row {new_start} to {i}")
            player_batch = Player.objects.filter(last_updated__lte=min_time_since_last_update)[:batch_size]
            self.update_player_batch(player_batch)
            new_start = i

        logger.info("Updating remaining players...")
        last_player_batch = Player.objects.filter(last_updated__lte=min_time_since_last_update)
        self.update_player_batch(last_player_batch)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all players"), ending="\n"
        )

    def update_player_batch(self, player_batch):

        logger.info("Fetching player batch's profiles and battlelogs from API...")
        tag_battlelog, tag_clubtag = self.get_all_players_profiles_and_battlelog(
            player_batch
        )
        logger.info("Creating matches from battlelog ...")
        for tag, battlelog in tag_battlelog.items():
            create_matches_from_battlelog(tag, battlelog)
        logger.info("Updating players clubs...")
        self.update_player_club(tag_clubtag)

        logger.info("Updating players' brawlclub rating...")
        for player in player_batch:
            player: Player
            player.last_updated = datetime.now(timezone.utc)
            player.update_brawlclub_rating()

    @async_to_sync
    async def get_all_players_profiles_and_battlelog(
        self, players
    ) -> Tuple[dict, dict]:
        """Get all players profiles and battlelogs.

        Keyword arguments:
        players -- Queryset of Player model

        Returns
        Tuple with :
        Dict matching player tag and battle log
        Dict matching player tag and club tag
        """
        players = await sync_to_async(list)(players)
        api_calls = []
        async with httpx.AsyncClient(timeout=3600) as client:
            for player in players:
                response = get_player_data(player.player_tag, client)
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
        async with httpx.AsyncClient(timeout=3600) as client:
            for tag, profile in tag_profile.items():
                if profile["club"]:
                    club_tag = profile["club"]["tag"]
                    tag_clubtag[tag] = club_tag
                else:
                    tag_clubtag[tag] = None
                response = get_player_battlelog(tag, client)
                api_calls.append(response)
            battlelogs = await asyncio.gather(*api_calls)
        tag_battlelog = {}
        for tag, battlelog in zip(tag_profile.keys(), battlelogs):
            tag_battlelog[tag] = battlelog

        logger.info(f"Number of to be updated players : {len(tag_profile.keys())}")
        return tag_battlelog, tag_clubtag

    def update_player_club(self, tag_clubtag: dict) -> None:
        """Update player's club.

        Keyword arguments:
        tag_clubtag -- Dict matching player tag and club tag
        """
        players_to_update = []
        clubs_to_create = []
        players_with_club_to_create = []
        for tag, clubtag in tag_clubtag.items():
            player = Player.objects.select_related("club").get(player_tag=tag)
            if clubtag is None:
                player.club = None
                players_to_update.append(player)
            elif player.club and player.club.club_tag == clubtag:
                continue
            else:
                club = Club.objects.filter(club_tag=clubtag).first()
                if club:
                    player.club = club
                    players_to_update.append(player)
                else:
                    clubs_to_create.append(clubtag)
                    players_with_club_to_create.append(player)

        if clubs_to_create:
            club_batch = self.create_club_batch(clubs_to_create)
            Club.objects.bulk_create(club_batch)
        if players_with_club_to_create:
            for player in players_with_club_to_create:
                player.club = Club.objects.get(club_tag=tag_clubtag[player.player_tag])
                players_to_update.append(player)
        Player.objects.bulk_update(players_to_update, ["club"])

    @async_to_sync
    async def create_club_batch(self, clubs_to_create: list) -> list:
        """Create club batch.

        Keyword arguments:
        clubs_to_create -- List of club tags
        """
        clubs_to_create = list(set(clubs_to_create))
        club_batch = []

        logger.info("Fetching club to create data from API...")
        async with httpx.AsyncClient(timeout=None) as client:
            tasks = []
            for club_tag in clubs_to_create:
                task = self.get_club_information(club_tag, client)
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
        logger.info(f"Creating {len(tasks)} clubs...")

        for club_information in responses:
            kwargs = {
                "club_tag": club_information["tag"],
                "club_name": club_information["name"],
                "club_description": club_information.get("description", ""),
                "club_type": club_information["type"],
                "club_tag": club_information["tag"],
                "trophies": club_information["trophies"],
                "required_trophies": club_information["requiredTrophies"],
            }
            club = Club(**kwargs)
            club_batch.append(club)

        return club_batch

    async def get_club_information(
        self, clubtag: str, client: httpx.AsyncClient
    ) -> dict:
        """Get club information.

        Keyword arguments:
        clubtag -- Club tag
        """
        clubtag = clubtag[1:]
        url = f"{brawl_api.base_url}clubs/%23{clubtag}"
        response = await client.get(url, headers=brawl_api.headers)
        response = response.json()
        return response
