from rest_framework import serializers
from .models import Player, Club


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
            "total_club_war_trophy_count",
            "club_league_winrate",
            "club_league_playrate",
            "club_league_teamplay_rate",
        )
        depth = 1


class ClubSerializer(serializers.ModelSerializer):
    """Serializer for the Club model."""

    avg_bcr = serializers.FloatField(read_only=True)
    nb_of_players = serializers.IntegerField(read_only=True)

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
