from django.urls import path
from . import views

app_name="homepage"

urlpatterns = [
    path('home/', views.home, name='home'), #placeholder
    path('landingpage/', views.landingpage, name='landingpage'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('listing/add/', views.add_listing, name='add_listing'),
    path('listing/overview', views.listing_overview, name='listing_overview'),
    #path('listing/<int:listing_id>', views.agreementResponse, name='agreement_response'),
]