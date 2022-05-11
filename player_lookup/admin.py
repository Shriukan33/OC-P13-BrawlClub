from django.contrib import admin
from . import models


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_tag', 'player_name', 'club', 'trophy_count')
    list_filter = ('club',)
    search_fields = ('player_tag', 'player_name')


class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_tag', 'club_name', 'club_type', 'trophies',
                    'required_trophies')
    list_filter = ('club_type',)
    search_fields = ('club_tag', 'club_name')


class BrawlMapAdin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class BrawlerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('mode', 'map_played', 'date')
    list_filter = ('mode', 'map_played')
    search_fields = ('mode', 'map_played')


class MatchIssueAdmin(admin.ModelAdmin):
    list_display = ("player", "brawler", "has_won", "trophies_won")
    list_filter = ("player", "brawler", "has_won")
    search_fields = ("player", "brawler")


admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.BrawlMap, BrawlMapAdin)
admin.site.register(models.Brawler, BrawlerAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.MatchIssue, MatchIssueAdmin)
admin.site.site_header = "Brawl Club Admin"
