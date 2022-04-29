from django import forms


class PlayerLookupForm(forms.Form):
    player_tag = forms.CharField(label='Player Tag', max_length=9,
                                 required=True)
