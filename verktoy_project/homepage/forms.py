from django import forms
from django.forms import ModelForm
from .models import Listing

#Skjema for å opprette Listing (annonse)
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'location', 'description']

#Skjema for å redigere Listing (annonse)
class EditListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'location', 'description']