from django import forms
from django.forms import ModelForm
from .models import Listing

#Skjema for å opprette Listing (annonse)
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'location','price', 'description']