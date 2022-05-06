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


admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.site_header = "Brawl Club Admin"
