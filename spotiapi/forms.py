from django.forms import ModelForm, TextInput
from .models import Artist


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Artist's name",
                                            'aria-label': "Artist Search-query", "aria-describedby": "button-addon2"})}
