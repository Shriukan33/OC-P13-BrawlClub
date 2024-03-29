from django.contrib import admin
from . import models


class PlayerInline(admin.TabularInline):
    model = models.Player


class MatchIssueInline(admin.TabularInline):
    model = models.MatchIssue


class PlayerAdmin(admin.ModelAdmin):
    inlines = [MatchIssueInline]
    list_display = (
        "player_tag",
        "player_name",
        "club",
        "trophy_count",
        "brawlclub_rating",
    )
    search_fields = ("player_tag", "player_name")
    readonly_fields = (
        "player_tag",
        "player_name",
        "club",
        "trophy_count",
        "last_updated",
        "default_date",
    )

    def has_change_permission(self, request, obj=None):
        return False


class PlayerHistoryAdmin(admin.ModelAdmin):
    list_display = ("player", "snapshot_date", "trophy_count")
    search_fields = ("player__player_name",)


class PlayersUpdateAdmin(admin.ModelAdmin):
    readonly_fields = ("last_update", "club_league_running")
    list_display = ("last_update", "club_league_running")


class ClubAdmin(admin.ModelAdmin):
    inlines = [
        PlayerInline,
    ]
    list_display = (
        "club_tag",
        "club_name",
        "club_type",
        "trophies",
        "required_trophies",
    )
    list_filter = ("club_type",)
    search_fields = ("club_tag", "club_name")


class BrawlMapAdin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


class BrawlerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


class MatchAdmin(admin.ModelAdmin):
    inlines = [
        MatchIssueInline,
    ]
    list_display = ("mode", "map_played", "date")
    list_filter = ("mode", "map_played")
    search_fields = ("mode", "map_played")

    def has_change_permission(self, request, obj=None):
        return False


class MatchIssueAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "brawler",
        "outcome",
        "trophies_won",
        "is_star_player",
        "played_with_clubmate",
    )
    list_filter = ("player", "brawler", "outcome")
    search_fields = ("player", "brawler")

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.PlayerHistory, PlayerHistoryAdmin)
admin.site.register(models.PlayersUpdate)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.BrawlMap, BrawlMapAdin)
admin.site.register(models.Brawler, BrawlerAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.MatchIssue, MatchIssueAdmin)
admin.site.site_header = "Brawl Club Admin"
