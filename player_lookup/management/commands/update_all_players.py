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
from player_lookup.utils import get_club_league_status

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Update every player in the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            "-f",
            action="store_true",
            help="Force update of all players",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        forced_update = options["force"]
        if forced_update:
            logger.info("Forced update")
        logger.info("Starting update_all_players command...")
        if not forced_update:
            min_time_since_last_update = datetime.now(timezone.utc) - timedelta(
                minutes=30
            )
        else:
            min_time_since_last_update = datetime.now(timezone.utc)

        self.club_league_running = get_club_league_status()
        total_player_count = Player.objects.count()
        player_count = Player.objects.filter(
            last_updated__lte=min_time_since_last_update
        ).count()
        logger.info(
            f"Found {player_count} players to update "
            f"in DB (Total : {total_player_count})"
        )
        batch_size = 999
        top_limit = player_count // batch_size * batch_size
        first_loop = True
        for i in range(0, top_limit + 1, batch_size):
            if first_loop:
                first_loop = False
                new_start = i
                continue

            logger.info(f"Updating row {new_start} to {i}")
            player_batch = Player.objects.filter(
                last_updated__lte=min_time_since_last_update
            )[:batch_size]
            self.update_player_batch(player_batch)
            new_start = i

        logger.info("Updating remaining players...")
        if not forced_update:
            last_player_batch = Player.objects.filter(
                last_updated__lte=min_time_since_last_update
            )
        else:
            last_player_batch = Player.objects.all()[top_limit:]

        self.update_player_batch(last_player_batch)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all players"), ending="\n"
        )

    def update_player_batch(self, player_batch):

        logger.info("Fetching player batch's profiles and battlelogs from API...")
        (
            tag_battlelog,
            tag_clubtag,
            tag_info,
        ) = self.get_all_players_profiles_and_battlelog(player_batch)
        logger.info("Creating matches from battlelog ...")
        for tag, battlelog in tag_battlelog.items():
            create_matches_from_battlelog(tag, battlelog)
        logger.info("Updating players clubs and infos...")
        player_batch = self.update_player_infos(tag_clubtag, tag_info)

        logger.info("Updating players' brawlclub rating...")
        player_batch_to_update = []
        for player in player_batch:
            player: Player
            player.last_updated = datetime.now(timezone.utc)
            if self.club_league_running:
                player.update_brawlclub_rating(save=False)
            player_batch_to_update.append(player)

        logger.info(f'Saving {len(player_batch_to_update)} players to DB...')
        Player.objects.bulk_update(
            player_batch_to_update,
            [
                "last_updated",
                "brawlclub_rating",
                "club_league_winrate",
                "club_league_playrate",
                "club_league_teamplay_rate",
                "player_name",
                "level",
                "trophy_count",
                "total_3v3_wins",
                "solo_wins",
                "duo_wins",
                "club",
            ],
        )
        logger.info("Done!")

    @async_to_sync
    async def get_all_players_profiles_and_battlelog(
        self, players
    ) -> Tuple[dict, dict, dict]:
        """Get all players profiles and battlelogs.

        Keyword arguments:
        players -- Queryset of Player model

        Returns
        Tuple with :
        Dict matching player tag and battle log
        Dict matching player tag and club tag
        Dict matching player tag and player info
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
        tag_info = {}
        async with httpx.AsyncClient(timeout=3600) as client:
            for tag, profile in tag_profile.items():
                if profile["club"]:
                    club_tag = profile["club"]["tag"]
                    tag_clubtag[tag] = club_tag
                else:
                    tag_clubtag[tag] = None
                # Update the general infos : Level, trophies, etc.
                tag_info[tag] = {
                    "player_name": profile.get("name", "Undefined"),
                    "level": profile.get("expLevel", 0),
                    "trophy_count": profile.get("trophies", 0),
                    "total_3v3_wins": profile.get("3vs3Victories", 0),
                    "solo_wins": profile.get("soloVictories", 0),
                    "duo_wins": profile.get("duoVictories", 0),
                }
                response = get_player_battlelog(tag, client)
                api_calls.append(response)
            battlelogs = await asyncio.gather(*api_calls)
        tag_battlelog = {}
        for tag, battlelog in zip(tag_profile.keys(), battlelogs):
            tag_battlelog[tag] = battlelog

        logger.info(f"Number of to be updated players : {len(tag_profile.keys())}")
        return tag_battlelog, tag_clubtag, tag_info

    def update_player_infos(self, tag_clubtag: dict, tag_infos: dict) -> list:
        """Update player's club and infos.

        Keyword arguments:
        tag_clubtag -- Dict matching player tag and club tag
        tag_infos -- Dict matching player tag and player info

        Returns:
        The updated player batch
        """
        players_to_update = []
        clubs_to_create = []
        players_with_club_to_create = []
        for tag, clubtag in tag_clubtag.items():
            player: Player = Player.objects.select_related("club").get(player_tag=tag)
            this_players_infos = tag_infos[tag]
            already_to_be_updated = False
            if this_players_infos:
                player.player_name = this_players_infos["player_name"]
                player.level = this_players_infos["level"]
                player.trophy_count = this_players_infos["trophy_count"]
                player.total_3v3_wins = this_players_infos["total_3v3_wins"]
                player.solo_wins = this_players_infos["solo_wins"]
                player.duo_wins = this_players_infos["duo_wins"]

            if clubtag is None:
                player.club = None
                players_to_update.append(player)
                continue
            if player.club and player.club.club_tag == clubtag:
                players_to_update.append(player)
                continue
            else:
                club = Club.objects.filter(club_tag=clubtag).first()
                if club:
                    player.club = club
                else:
                    clubs_to_create.append(clubtag)
                    players_with_club_to_create.append(player)
                    already_to_be_updated = True

            if not already_to_be_updated:
                players_to_update.append(player)

        if clubs_to_create:
            club_batch = self.create_club_batch(clubs_to_create)
            Club.objects.bulk_create(club_batch)
        if players_with_club_to_create:
            for player in players_with_club_to_create:
                player.club = Club.objects.get(club_tag=tag_clubtag[player.player_tag])
                players_to_update.append(player)

        return players_to_update

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
