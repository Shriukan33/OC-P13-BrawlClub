from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "player_lookup"

urlpatterns = []

drf_patterns = [
    path(
        "api/club-finder/results",
        views.ClubFinderResultsView.as_view(),
        name="club_finder_results",
    ),
    path(
        "api/club-members/<str:club_tag>",
        views.ClubMembersView.as_view(),
        name="club_members",
    ),
    path(
        "api/leaderboard/<str:entity>/",
        views.LeaderBoardView.as_view(),
        name="leaderboard",
    ),
    path(
        "api/player/areagraph/<str:player_tag>",
        views.PlayerAreaGraphView.as_view(),
        name="player_areagraph",
    ),
    path(
        "api/search/<str:tag>",
        views.SearchUnknownEntityView.as_view(),
        name="search_unknown",
    ),
    path(
        "api/<str:entity>/<str:tag>",
        views.SingleEntityView.as_view(),
        name="search_specific",
    ),
]

urlpatterns += format_suffix_patterns(drf_patterns)
