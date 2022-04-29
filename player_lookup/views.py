from django.views.generic import FormView

from .forms import PlayerLookupForm


class PlayerLookupView(FormView):
    template_name = 'player_lookup/player_lookup.html'
    form_class = PlayerLookupForm
