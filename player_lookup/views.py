from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import PlayerLookupForm
from .brawlstars_api import BrawlAPi

brawl_api = BrawlAPi()


class PlayerLookupView(FormView):
    template_name = 'player_lookup/player_lookup.html'
    form_class = PlayerLookupForm
    success_url = 'player_lookup:player_page'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        player_tag = form.cleaned_data['player_tag']
        return HttpResponseRedirect(self.get_success_url(player_tag))

    def get_success_url(self, player_tag) -> str:
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. "
                                       "Provide a success_url.")
        success_url = reverse_lazy(self.success_url, args=[player_tag])
        return success_url


class PlayerPageView(TemplateView):
    template_name = 'player_lookup/player_page.html'

    def get_context_data(self, **kwargs):
        """Displays the stats of the player."""
        player_tag = kwargs['player_tag']
        player_data = brawl_api.get_player_stats(player_tag)
        context = super().get_context_data(**kwargs)
        context['player_data'] = player_data
        return context
