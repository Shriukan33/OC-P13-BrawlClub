from django import forms


def validate_player_tag(value: str):
    if not value.startswith("#"):
        raise forms.ValidationError("Player tag must start with #")
    if any(not char.isalnum() for char in value[1:]):
        raise forms.ValidationError("Player tag must only contain "
                                    "alphanumeric characters")
    if len(value) < 9:
        raise forms.ValidationError("Player tag must be at least 9 "
                                    "characters long")


class PlayerLookupForm(forms.Form):
    player_tag = forms.CharField(label='Player Tag', max_length=9,
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Ex : #2RQRYVOL'}),
                                 validators=[validate_player_tag])
