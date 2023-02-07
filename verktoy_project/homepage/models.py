from django.db import models
from django.contrib.auth.models import  User, Group

# Create your models here.

class Listing(models.Model):
    owner = models.ForeignKey(User, verbose_name = 'User', on_delete=models.CASCADE) #user burde kanskje endres til settings.AUTH_USER_MODEL. må i så fall django.conf import settings
    title = models.CharField(max_length=50)
    loaned = models.BooleanField(default=False)
    location = models.CharField(max_length=100) #burde kanskje være annet enn CharField. Gjør det vanskelig å sortere etter denne attributten
    description = models.TextField()

    #For under, se https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices.
    #Heltall for raskere sortering.
    SW = 1
    PT = 2
    WD = 3
    CT = 4
    OT = 5
    CATEGORY_CHOICES = (
        (SW, 'Sag'),
        (PT, 'Maling'),
        (WD, 'Sveising'),
        (CT, 'Kutt/Kapping'),
        (OT, 'Annet'),
    )
    category = models.PositiveSmallIntegerField(
        choices = CATEGORY_CHOICES,
        default = OT,
    )

