from django.db import models
from django.forms import ValidationError


def limit_number_of_players(value):
    if Player.objects.filter(club__id=value).count() > 30:
        raise ValidationError(
            "The number of players in a club must be less than 30.")


class Player(models.Model):

    player_tag = models.CharField(max_length=9, primary_key=True)
    player_name = models.CharField(max_length=50)
    trophy_count = models.IntegerField(default=0)
    club = models.ForeignKey('Club', on_delete=models.SET_NULL, null=True,
                             validators=[limit_number_of_players])
    total_club_war_trophy_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player_name} ({self.player_tag})"


class Club(models.Model):
    """Clubs are groups of players up to 30 persons"""

    club_tag = models.CharField(max_length=9, primary_key=True)
    club_name = models.CharField(max_length=50)
    club_description = models.CharField(max_length=100, blank=True)
    club_type = models.CharField(max_length=20, default="open")
    required_trophies = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)

    def __str__(self):
        return self.club_name


class Brawler(models.Model):
    """Brawlers are characters the players can choose from."""
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='brawlers/')

    def __str__(self):
        return self.name


class BrawlMap(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='maps/')

    def __str__(self):
        return self.name


class Match(models.Model):

    # The match id is build with the following format:
    # <star_player_tag_without_#><timestamp_in_epoch_seconds>
    match_id = models.CharField(max_length=18, primary_key=True)
    # Brawlball, Gem grab, Knockout ...
    mode = models.CharField(max_length=20)
    # Map
    map_played = models.ForeignKey(BrawlMap, on_delete=models.SET_NULL,
                                   null=True)
    # Power match or normal match
    battle_type = models.CharField(max_length=20)
    # Provided in the API
    date = models.DateTimeField()

    def __str__(self):
        return (f"{self.battle_type} - {self.mode} "
                f"- {self.date.strftime('%d/%m/%Y')}")


class MatchIssue(models.Model):

    class MatchOutcomes(models.TextChoices):
        WIN = 'WIN', 'Win'
        LOSS = 'LOSS', 'Loss'
        DRAW = 'DRAW', 'Draw'
        UNKNOWN = 'UNKNOWN', 'Unknown'

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=7, choices=MatchOutcomes.choices,
                               default=MatchOutcomes.UNKNOWN)
    trophies_won = models.IntegerField(default=0)
    is_star_player = models.BooleanField(default=False)
    played_with_clubmate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player} - {self.brawler} - {self.match}"
