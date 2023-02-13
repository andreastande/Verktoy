from django.test import TestCase
from homepage.models import Listing
from users.models import User

# Create your tests here.

class ListingTests(TestCase):
    def test_createListing(self):
        user1 = User.objects.create_user(username="testuser", password="123")
        listing1 = Listing.objects.create(  owner=user1,
                                            title="Sag", 
                                            loaned=True, 
                                            location="Trondheim", 
                                            description="Hei", 
                                            category=1)

        testUser = listing1.owner
        self.assertEqual(user1.username, testUser.username)
        self.assertEqual(user1.password, testUser.password)

        self.assertEqual("Sag", listing1.title)
        self.assertTrue(listing1.loaned)
        self.assertEqual("Trondheim", listing1.location)
        self.assertEqual("Hei", listing1.description)
        self.assertEqual(1, listing1.category)

    '''
    Tester som mangler:
        - Ulike tester som skal faile ved tittel, beskrivelse, kategori osv
          som ikke følger reglene til Listing-klassen. Typ lengde osv
    '''