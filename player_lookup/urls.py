from django.urls import path
from . import views

app_name = 'player_lookup'

urlpatterns = [
    path('', views.PlayerLookupView.as_view(), name='index'),
    path('player_page/<str:player_tag>', views.PlayerPageView.as_view(),
         name='player_page'),
    path('club_members/<str:club_tag>', views.update_club_members)
]
