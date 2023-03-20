from django import forms
from django.forms import ModelForm
from .models import Listing, Review
from .models import UserDefinedList


#Skjema for å opprette Listing (annonse)
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'image', 'category', 'location', 'price', 'description']

#Skjema for å redigere Listing (annonse)
class EditListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'image', 'category', 'location', 'price', 'description']

# class PrependListingToList(ModelForm):
#     class Meta:
#         model = UserDefinedList
#         forms.ChoiceField

class ReviewForm(ModelForm):
    class Meta:
        Model = Review
        fields = ['title', 'review', 'rating']
