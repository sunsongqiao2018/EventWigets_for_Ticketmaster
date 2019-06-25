from django.forms import ModelForm, TextInput
from django import forms
from .models import Event


class SizeForm(forms.Form):

    event_size = forms.IntegerField(label='event size you want', max_value=200, min_value=1, widget=forms.NumberInput(
                attrs={'size': '50'}))


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control', 'placeholder': "Event's name",
                                            'aria-label': "Event Search-query", "aria-describedby": "button-addon2"})}
