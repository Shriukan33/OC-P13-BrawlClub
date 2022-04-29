from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerLookupView.as_view(), name='player_lookup'),
]
