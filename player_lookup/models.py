from datetime import datetime, timezone
from typing import TYPE_CHECKING
import logging

from django.db import models
from freezegun import freeze_time

from player_lookup.utils import (
    get_number_of_weeks_since_date,
    get_this_weeks_number_of_available_tickets,
)
from player_lookup.brawlstars_api import BrawlAPi

if TYPE_CHECKING:  # pragma: no cover
    from django.db.models.query import QuerySet

logger = logging.getLogger("django")

# Used to be a validation function
# Because migration 0001_initial.py is using
# player_lookup.models.limit_number_of_players to create the Player model,
# the migration process expects this module to have a limit_number_of_players
# attribute. Although it's not used, Django will still look for it, so we leave
# it here.
limit_number_of_players = None


class Player(models.Model):

    player_tag = models.CharField(max_length=15, primary_key=True)
    player_name = models.CharField(max_length=50)
    trophy_count = models.IntegerField(default=0)
    club = models.ForeignKey(
        "Club",
        on_delete=models.SET_NULL,
        null=True,
    )
    level = models.IntegerField(default=0)
    total_3v3_wins = models.IntegerField(default=0)
    solo_wins = models.IntegerField(default=0)
    duo_wins = models.IntegerField(default=0)
    total_club_war_trophy_count = models.IntegerField(default=0)
    brawlclub_rating = models.FloatField(default=0)
    club_league_winrate = models.FloatField(default=0)
    # Number of tickets spent on total possible
    club_league_playrate = models.FloatField(default=0)
    # Frequence of game played with a clubmate
    club_league_teamplay_rate = models.FloatField(default=0)
    last_updated = models.DateTimeField(null=True, blank=True)

    # Date at which we start counting the playrate
    default_date = models.DateTimeField(auto_now_add=True)

    # Searched players will get updated more often
    # The first time a club or a player is searched, this flag is set to True
    has_been_searched = models.BooleanField(default=False)

    # The number of tickets the player could spend right now
    number_of_available_tickets = models.IntegerField(default=0)

    def __str__(self):  # pragma: no cover
        return f"{self.player_name} ({self.player_tag})"

    def update_brawlclub_rating(self, save: bool = True):
        """Update player's club league rating.

        Brawlclub rating rates a player according to three parameters :
        - The number of tickets spent per week
        - The frequence the player plays with a club mate
        - The win rate
        """
        # Do not update if the player is not in a club
        # Players under 900 trophies don't have clubs
        if not self.club or self.trophy_count < 900:
            return
        # TODO
        # Multiple fetch and filters are done inside those functions
        # Maybe consider use of prefetch_related or simply cache the results
        # before calling those functions
        rate = (
            self.get_playrate() * 50
            + self.get_teamplay_rate() * 30
            + self.get_win_rate() * 20
        )
        self.brawlclub_rating = rate
        if save:
            self.save(
                update_fields=[
                    "brawlclub_rating",
                    "club_league_playrate",
                    "club_league_winrate",
                    "club_league_teamplay_rate",
                    "last_updated",
                ]
            )

    def get_win_rate(self) -> float:
        """Get the win rate of the player.

        Args:
            since (datetime): The date since when the win rate is calculated.
        """
        winrate = 0

        if self.default_date:
            all_wins = MatchIssue.objects.filter(
                player=self, match__date__gte=self.default_date, outcome="WIN"
            ).count()
            all_losses = MatchIssue.objects.filter(
                player=self, match__date__gte=self.default_date, outcome="LOSS"
            ).count()
        else:
            all_wins = MatchIssue.objects.filter(player=self, outcome="WIN").count()
            all_losses = MatchIssue.objects.filter(player=self, outcome="LOSS").count()

        if all_wins + all_losses == 0:
            self.club_league_winrate = 0
            return 0

        winrate = all_wins / (all_wins + all_losses)
        self.club_league_winrate = winrate
        return winrate

    def get_teamplay_rate(self) -> float:
        """Get the teamplay rate of the player.

        Args:
            since (datetime): The date since when the teamplay rate is calculated.

        Returns:
            float: The teamplay rate of the player.
        """
        teamplay_rate = 0
        if self.default_date:
            played_with_clubmate = MatchIssue.objects.filter(
                player=self,
                match__date__gte=self.default_date,
                played_with_clubmate=True,
            ).count()
            all_matches = MatchIssue.objects.filter(
                player=self, match__date__gte=self.default_date
            ).count()

        else:
            played_with_clubmate = MatchIssue.objects.filter(
                player=self, played_with_clubmate=True
            ).count()
            all_matches = MatchIssue.objects.filter(player=self).count()

        if all_matches == 0:
            self.club_league_teamplay_rate = 0
            return 0

        teamplay_rate = played_with_clubmate / all_matches
        self.club_league_teamplay_rate = teamplay_rate
        return teamplay_rate

    def get_playrate(self) -> float:
        """
        Get the rate of the number of tickets spent on the number of tickets available.

        Every other week, one has 14 tickets to spend, from wednesday to wednesday.
        """
        with freeze_time(self.default_date.strftime("%Y-%m-%d")):
            first_weeks_number_of_tickets = get_this_weeks_number_of_available_tickets()

        this_weeks_number_of_available_tickets = (
            get_this_weeks_number_of_available_tickets()
        )

        club_league_weeks_since = get_number_of_weeks_since_date(self.default_date)

        all_power_matches_since_count = MatchIssue.objects.filter(
            player=self,
            match__date__gte=self.default_date,
            match__battle_type="Power Match",
        ).count()
        all_normal_matches_since_count = (
            MatchIssue.objects.filter(
                player=self, match__date__gte=self.default_date
            ).count()
            - all_power_matches_since_count
        )
        total_tickets_spent = (
            all_power_matches_since_count * 2 + all_normal_matches_since_count
        )

        playrate = total_tickets_spent / (
            first_weeks_number_of_tickets
            + club_league_weeks_since * 14
            + this_weeks_number_of_available_tickets
        )
        self.club_league_playrate = playrate
        return playrate

    def create_player_history_instance(self):
        """Create a player history instance for the player."""
        return PlayerHistory(
            player=self,
            trophy_count=self.trophy_count,
            total_club_war_trophy_count=self.total_club_war_trophy_count,
            brawlclub_rating=self.brawlclub_rating,
            club_league_playrate=self.club_league_playrate,
            club_league_winrate=self.club_league_winrate,
            club_league_teamplay_rate=self.club_league_teamplay_rate,
            snapshot_date=datetime.now(timezone.utc),
        )


def update_player_batch_remaining_tickets(
    player_batch: "QuerySet[Player]",
    today_number_of_tickets: int,
    last_club_league_day_start: datetime,
) -> list:
    """Update the remaining tickets of a batch of players.

    Args:
        player_batch (QuerySet[Player]): A batch of players.

    Returns:
        list: A list of players with their remaining tickets updated.
    """
    # We're fetching all matches from the last club league day for current batch
    # This means possibly fetching up to 6 matches per player
    player_batch_match_issues = MatchIssue.objects.select_related("match").filter(
        player__in=player_batch, match__date__gte=last_club_league_day_start
    )
    updated_players = []
    for player in player_batch:
        tickets_spent = 0
        this_players_match_issues = player_batch_match_issues.filter(player=player)
        all_power_matches_count = this_players_match_issues.filter(
            player=player,
            match__date__gte=last_club_league_day_start,
            match__battle_type="Power Match",
        ).count()
        # Each power match uses 2 tickets
        tickets_spent += all_power_matches_count * 2
        # Each normal match uses 1 ticket
        all_normal_matches_count = (
            this_players_match_issues.count() - all_power_matches_count
        )
        tickets_spent += all_normal_matches_count

        player.number_of_available_tickets = today_number_of_tickets - tickets_spent

        updated_players.append(player)
    return updated_players


class PlayerHistory(models.Model):
    """Make a snapshot of player's current stats"""

    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trophy_count = models.IntegerField(default=0)
    total_club_war_trophy_count = models.IntegerField(default=0)
    brawlclub_rating = models.FloatField(default=0)
    club_league_winrate = models.FloatField(default=0)
    club_league_playrate = models.FloatField(default=0)
    club_league_teamplay_rate = models.FloatField(default=0)
    snapshot_date = models.DateTimeField()

    def __str__(self):  # pragma: no cover
        return (
            f"{self.player.player_name} ({self.player.player_tag})"
            f" - {self.snapshot_date}"
        )


class Club(models.Model):
    """Clubs are groups of players up to 30 persons"""

    club_tag = models.CharField(max_length=15, primary_key=True)
    club_name = models.CharField(max_length=50)
    club_description = models.CharField(max_length=200, blank=True)
    club_type = models.CharField(max_length=20, default="open")
    required_trophies = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    # Searched clubs are updated more frequently
    # The first time a club or a player is searched, this flag is set to True
    has_been_searched = models.BooleanField(default=False)

    def __str__(self):  # pragma: no cover
        return self.club_name

    # Dev env only, not used in production
    def get_average_brawlclub_rating(self):  # pragma: no cover
        """Get the average brawlclub rating of the club."""
        return self.player_set.aggregate(models.Avg("brawlclub_rating"))[
            "brawlclub_rating__avg"
        ]

    # Dev env only, not used in production
    def update_all_club_members_ratings(self):  # pragma: no cover
        """Update all club members ratings."""
        for player in self.player_set.all():
            player.update_brawlclub_rating()

    # Dev env only, not used in production
    def update_members(self):  # pragma: no cover
        """Update the club's member list
        This method is meant to update a single instance, on demand.
        """
        api = BrawlAPi()
        members = api.get_club_members_tag_list(self.club_tag)
        for player_tag in members:
            player = Player.objects.get_or_create(player_tag=player_tag)[0]
            player.club = self
            player.save()

        for player in self.player_set.all().values_list("player_tag", flat=True):
            if player not in members:
                player = Player.objects.get(player_tag=player)
                player.club = None
                player.save()


class Brawler(models.Model):
    """Brawlers are characters the players can choose from."""

    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="brawlers/")

    def __str__(self):  # pragma: no cover
        return self.name


class BrawlMap(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="maps/")

    def __str__(self):  # pragma: no cover
        return self.name


class Match(models.Model):

    # The match id is build with the following format:
    # <star_player_tag_without_#><timestamp_in_epoch_seconds>
    match_id = models.CharField(max_length=30, primary_key=True)
    # Brawlball, Gem grab, Knockout ...
    mode = models.CharField(max_length=20)
    # Map
    map_played = models.ForeignKey(BrawlMap, on_delete=models.SET_NULL, null=True)
    # Power match or normal match
    battle_type = models.CharField(max_length=20)
    # Provided in the API
    date = models.DateTimeField()

    def __str__(self):  # pragma: no cover
        return (
            f"{self.battle_type} - {self.mode} " f"- {self.date.strftime('%d/%m/%Y')}"
        )


class MatchIssue(models.Model):
    class MatchOutcomes(models.TextChoices):
        WIN = "WIN", "Win"
        LOSS = "LOSS", "Loss"
        DRAW = "DRAW", "Draw"
        UNKNOWN = "UNKNOWN", "Unknown"

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    outcome = models.CharField(
        max_length=7, choices=MatchOutcomes.choices, default=MatchOutcomes.UNKNOWN
    )
    trophies_won = models.IntegerField(default=0)
    is_star_player = models.BooleanField(default=False)
    played_with_clubmate = models.BooleanField(default=False)

    def __str__(self):  # pragma: no cover
        return f"{self.player} - {self.brawler} - {self.match}"
