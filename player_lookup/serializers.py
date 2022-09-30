from rest_framework import serializers
from .models import Player, Club, PlayerHistory
from django.db.models import Avg, Count


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for the Player model."""

    class Meta:
        model = Player
        fields = (
            "player_tag",
            "player_name",
            "brawlclub_rating",
            "trophy_count",
            "club",
            "level",
            "total_3v3_wins",
            "solo_wins",
            "duo_wins",
            "total_club_war_trophy_count",
            "club_league_winrate",
            "club_league_playrate",
            "club_league_teamplay_rate",
        )
        read_only_fields = (
            "player_tag",
            "player_name",
            "brawlclub_rating",
            "trophy_count",
            "club",
            "level",
            "total_3v3_wins",
            "solo_wins",
            "duo_wins",
            "total_club_war_trophy_count",
            "club_league_winrate",
            "club_league_playrate",
            "club_league_teamplay_rate",
        )
        depth = 1


class PlayerHistorySerializer(serializers.ModelSerializer):
    """Serializer for the PlayerHistory model."""

    class Meta:
        model = PlayerHistory
        fields = (
            "snapshot_date",
            "brawlclub_rating",
        )

class ClubSerializer(serializers.ModelSerializer):
    """Serializer for the Club model."""

    class Meta:
        model = Club
        fields = (
            "club_tag",
            "club_name",
            "club_description",
            "club_type",
            "required_trophies",
            "trophies",
            "avg_bcr",
            "nb_of_players",
            "avg_win_rate",
            "avg_teamplay_rate",
            "avg_play_rate",
        )
        read_only_fields = (
            "club_tag",
            "club_name",
            "club_description",
            "club_type",
            "required_trophies",
            "trophies",
            "avg_bcr",
            "nb_of_players",
        )
        depth = 1

    avg_bcr = serializers.SerializerMethodField()
    nb_of_players = serializers.SerializerMethodField()
    avg_win_rate = serializers.SerializerMethodField()
    avg_play_rate = serializers.SerializerMethodField()
    avg_teamplay_rate = serializers.SerializerMethodField()

    def get_avg_bcr(self, obj):
        """Return the average BCR of the club."""
        avg_bcr = (
            Club.objects.filter(club_tag=obj.club_tag)
            .annotate(avg_bcr=Avg("player__brawlclub_rating"))
            .first()
            .avg_bcr
        )
        return round(avg_bcr, 2)

    def get_nb_of_players(self, obj):
        """Return the number of players in the club."""
        nb_of_players = (
            Club.objects.filter(club_tag=obj.club_tag)
            .annotate(nb_of_players=Count("player"))
            .first()
            .nb_of_players
        )
        return nb_of_players

    def get_avg_win_rate(self, obj):
        """Return the average win rate of the club."""
        avg_win_rate = (
            Club.objects.filter(club_tag=obj.club_tag)
            .annotate(avg_win_rate=Avg("player__club_league_winrate"))
            .first()
            .avg_win_rate
        )
        return round(avg_win_rate, 2)

    def get_avg_play_rate(self, obj):
        """Return the average play rate of the club."""
        avg_play_rate = (
            Club.objects.filter(club_tag=obj.club_tag)
            .annotate(avg_play_rate=Avg("player__club_league_playrate"))
            .first()
            .avg_play_rate
        )
        return round(avg_play_rate, 2)

    def get_avg_teamplay_rate(self, obj):
        """Return the average teamplay rate of the club."""
        avg_teamplay_rate = (
            Club.objects.filter(club_tag=obj.club_tag)
            .annotate(avg_teamplay_rate=Avg("player__club_league_teamplay_rate"))
            .first()
            .avg_teamplay_rate
        )
        return round(avg_teamplay_rate, 2)
