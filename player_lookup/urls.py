from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'player_lookup'

urlpatterns = [
    path('update_clubs/', views.update_all_clubs, name='update_clubs'),
    path('club_members/<str:club_tag>', views.update_club_members),
]

drf_patterns = [
    path("api/leaderboard/<str:entity>/", views.LeaderBoardView.as_view()),
    path("api/club-members/<str:club_tag>", views.ClubMembersView.as_view()),
    path("api/search/<str:tag>", views.SearchUnknownEntityView.as_view()),
    path("api/<str:entity>/<str:tag>", views.SingleEntityView.as_view()),
]

urlpatterns += format_suffix_patterns(drf_patterns)
