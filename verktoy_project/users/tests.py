from django.test import TestCase
from homepage.models import Listing
from .models import Profile
# Create your tests here.

def create_listing(owner, title, loaned, location, description):
    return Listing.objects.create(owner, title, loaned, location, description)

def create_profile():
    return Profile.objects.create()


class OwnListingsTest(TestCase):
    def only_your_listings_show_up(self):
        user1=create_profile()
        user2=create_profile()
        listing1=create_listing(user1, "listing 1", False, "test", "test")
        listing2=create_listing(user1, "listing 1", False, "test", "test")
        listing3=create_listing(user2, "listing 1", False, "test", "test")
        
        for listing in user1.own_listings():
            self.assertTrue(listing.owner==user1)
