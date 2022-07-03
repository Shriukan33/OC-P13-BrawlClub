from django.urls import path
from . import views

app_name = 'player_lookup'

urlpatterns = [
    path('club_members/<str:club_tag>', views.update_club_members),
    path("api/player/<str:player_tag>", views.update_player_profile),
]
