import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import logging
import time
import httpx
from typing import Tuple
from django.core.management.base import BaseCommand
from django.db.models import Q, QuerySet
from asgiref.sync import sync_to_async, async_to_sync
from player_lookup.models import (
    BrawlMap,
    Brawler,
    Club,
    MatchIssue,
    Player,
    PlayersUpdate,
)
from player_lookup.models import update_player_batch_remaining_tickets
from player_lookup.views import (
    create_matches_from_battlelog,
    get_player_battlelog,
    get_player_data,
    brawl_api,
)
from player_lookup.utils import (
    get_club_league_status,
    get_last_club_league_day_start,
    get_today_number_of_remaining_tickets,
)

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
            min_time_since_last_update = datetime.now(timezone.utc) - timedelta(hours=8)
        else:
            min_time_since_last_update = datetime.now(timezone.utc)

        # Because these are small tables, to save on number of queries, we'll
        # fetch all the data we need in memory
        self.all_brawlers = Brawler.objects.all()
        self.all_maps = BrawlMap.objects.all()

        # last_club_league_day and today_number_of_remaining_tickets are used
        # to calculate the number of remaining tickets for each player
        self.last_club_league_day = get_last_club_league_day_start()
        self.today_number_of_remaining_tickets = get_today_number_of_remaining_tickets()

        # Because computing the Brawlclub rating is a bit expensive, we do it
        # only while the club league is running
        self.club_league_running = get_club_league_status()
        if not self.club_league_running:
            logger.info("Club league is not running, updating remaining tickets to 0")
            Player.objects.update(number_of_available_tickets=0)
            queryset = Player.objects.filter(
                Q(last_updated__lte=min_time_since_last_update) | Q(last_updated=None),
                number_of_available_tickets__gt=0,
            ).order_by("-brawlclub_rating", "last_updated")
        else:
            logger.info("Replenishing players' tickets...")
            Player.objects.filter(
                Q(last_updated__lt=self.last_club_league_day)
                | (Q(last_updated__isnull=True))
            ).update(number_of_available_tickets=self.today_number_of_remaining_tickets)
            queryset = Player.objects.filter(
                Q(last_updated__lte=min_time_since_last_update) | Q(last_updated=None)
            ).order_by("-brawlclub_rating", "last_updated")

        for start, end, total, qs in self.batch_qs(queryset, 500):
            logger.info(
                f"Updating row {start} to {end} on {total} ({start/total*100:.2f}%)"
            )
            self.update_player_batch(qs)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all players"), ending="\n"
        )

    def batch_qs(self, qs: "QuerySet[Player]", batch_size):
        """Returns a (start, end, total, queryset) tuple for each batch in the given
        queryset.

        Usage:
            # Make sure to order your querset
            article_qs = Article.objects.order_by('id')
            for start, end, total, qs in batch_qs(article_qs):
                print("Now processing %s - %s of %s" % (start + 1, end, total))
                for article in qs:
                    print(article.body)
        """
        total = qs.count()
        for start in range(0, total, batch_size):
            end = start + batch_size
            yield (start, end, total, qs[start:end])

    def update_player_batch(self, player_batch):

        time_start = time.time()
        logger.info("Fetching player batch's profiles and battlelogs from API...")
        (
            tag_battlelog,
            tag_clubtag,
            tag_info,
        ) = self.get_all_players_profiles_and_battlelog(player_batch)

        logger.info("Creating matches from battlelog ...")
        match_batch = []
        for tag, battlelog in tag_battlelog.items():
            matches = create_matches_from_battlelog(
                tag, battlelog, self.all_brawlers, self.all_maps
            )
            match_batch.extend(matches)

        if match_batch:
            logger.info(f"Saving {len(match_batch)} matches...")
            MatchIssue.objects.bulk_create(match_batch)

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

        if self.club_league_running:
            logger.info("Updating players' remaining tickets...")
            player_batch_to_update = update_player_batch_remaining_tickets(
                player_batch_to_update,
                self.today_number_of_remaining_tickets,
                self.last_club_league_day,
            )

        logger.info(f"Saving {len(player_batch_to_update)} players to DB...")
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
                "number_of_available_tickets",
            ],
        )
        time_end = time.time()
        logger.info(f"Done! Time elapsed : {time_end - time_start}")

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
