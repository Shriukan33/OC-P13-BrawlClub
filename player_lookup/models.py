from datetime import datetime, timezone
import logging

from django.db import models
from django.forms import ValidationError

from player_lookup.utils import (
    get_number_of_weeks_since_date,
    get_this_weeks_number_of_available_tickets,
)
from player_lookup.brawlstars_api import BrawlAPi

logger = logging.getLogger("django")


def limit_number_of_players(value):
    if Player.objects.filter(club__id=value).count() > 30:
        raise ValidationError("The number of players in a club must be less than 30.")


class Player(models.Model):

    player_tag = models.CharField(max_length=15, primary_key=True)
    player_name = models.CharField(max_length=50)
    trophy_count = models.IntegerField(default=0)
    club = models.ForeignKey(
        "Club",
        on_delete=models.SET_NULL,
        null=True,
        validators=[limit_number_of_players],
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
    default_date = datetime(year=2022, month=7, day=20, tzinfo=timezone.utc)

    def __str__(self):
        return f"{self.player_name} ({self.player_tag})"

    def update_brawlclub_rating(self, save: bool = True):
        """Update player's club league rating.

        Brawlclub rating rates a player according to three parameters :
        - The number of tickets spent per week
        - The frequence the player plays with a club mate
        - The win rate
        """
        # Do not update if the player is not in a club
        if not self.club:
            return
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

    def get_brawclub_rating(self, since: datetime = default_date) -> float:
        """Get the brawlclub rating of the player.

        Args:
            since (datetime): The date since when the brawlclub rating is calculated.
        """
        return (
            self.get_win_rate(since) * 50
            + self.get_teamplay_rate(since) * 30
            + self.get_playrate(since) * 20
        )

    def get_win_rate(self, since: datetime = default_date) -> float:
        """Get the win rate of the player.

        Args:
            since (datetime): The date since when the win rate is calculated.
        """
        winrate = 0

        if since:
            all_wins = MatchIssue.objects.filter(
                player=self, match__date__gte=since, outcome="WIN"
            ).count()
            all_losses = MatchIssue.objects.filter(
                player=self, match__date__gte=since, outcome="LOSS"
            ).count()
        else:
            all_wins = MatchIssue.objects.filter(player=self, outcome="WIN").count()
            all_losses = MatchIssue.objects.filter(player=self, outcome="LOSS").count()

        if all_wins + all_losses == 0:
            return 0

        winrate = all_wins / (all_wins + all_losses)
        self.club_league_winrate = winrate
        return winrate

    def get_teamplay_rate(self, since: datetime = default_date) -> float:
        """Get the teamplay rate of the player.

        Args:
            since (datetime): The date since when the teamplay rate is calculated.

        Returns:
            float: The teamplay rate of the player.
        """
        teamplay_rate = 0
        if since:
            played_with_clubmate = MatchIssue.objects.filter(
                player=self, match__date__gte=since, played_with_clubmate=True
            ).count()
            all_matches = MatchIssue.objects.filter(
                player=self, match__date__gte=since
            ).count()

        else:
            played_with_clubmate = MatchIssue.objects.filter(
                player=self, played_with_clubmate=True
            ).count()
            all_matches = MatchIssue.objects.filter(player=self).count()

        if all_matches == 0:
            return 0

        teamplay_rate = played_with_clubmate / all_matches
        self.club_league_teamplay_rate = teamplay_rate
        return teamplay_rate

    def get_playrate(self, since: datetime = default_date) -> float:
        """
        Get the rate of the number of tickets spent on the number of tickets available.

        Every other week, one has 14 tickets to spend, from wednesday to wednesday.
        """
        if not since:
            since = datetime(year=2022, month=1, day=1, tzinfo=timezone.utc)

        this_weeks_number_of_available_tickets = (
            get_this_weeks_number_of_available_tickets()
        )

        # Because a club league is likely to be going on at any time, we count
        # the results to end of last week's league and add to that the partial
        # results of this week.
        # The formula goes as follows:
        # total tickets spent since date / (number of whole weeks since date * 14)
        # + partial results

        club_league_weeks_since = get_number_of_weeks_since_date(since)

        all_power_matches_since_count = MatchIssue.objects.filter(
            player=self, match__date__gte=since, match__battle_type="Power Match"
        ).count()
        all_normal_matches_since_count = (
            MatchIssue.objects.filter(player=self, match__date__gte=since).count()
            - all_power_matches_since_count
        )
        total_tickets_spent = (
            all_power_matches_since_count * 2 + all_normal_matches_since_count
        )

        playrate = total_tickets_spent / (
            club_league_weeks_since * 14 + this_weeks_number_of_available_tickets
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

    def __str__(self):
        return (f"{self.player.player_name} ({self.player.player_tag})"
                f" - {self.snapshot_date}")


class Club(models.Model):
    """Clubs are groups of players up to 30 persons"""

    club_tag = models.CharField(max_length=15, primary_key=True)
    club_name = models.CharField(max_length=50)
    club_description = models.CharField(max_length=200, blank=True)
    club_type = models.CharField(max_length=20, default="open")
    required_trophies = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.club_name

    def get_average_brawlclub_rating(self):
        """Get the average brawlclub rating of the club."""
        return self.player_set.aggregate(models.Avg("brawlclub_rating"))[
            "brawlclub_rating__avg"
        ]

    def update_all_club_members_ratings(self):
        """Update all club members ratings."""
        for player in self.player_set.all():
            player.update_brawlclub_rating()

    def update_members(self):
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

    def __str__(self):
        return self.name


class BrawlMap(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="maps/")

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
        return f"{self.player} - {self.brawler} - {self.match}"
