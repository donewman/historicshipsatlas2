from django import forms
from atlas.models import Ship, Type, City, Country, Status, Use, Owner

# Basic search form--appears on all pages
class BasicSearchForm(forms.Form):
    keywords = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'input-group-field'}))
