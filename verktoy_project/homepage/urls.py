from django.urls import path
from . import views

app_name="home"

urlpatterns = [
    path('home', views.home, name='home'), #placeholder
    path('listing/<int:annonse_id>', views.listing, name='listing'),
    path('listing/add/', views.add_listing, name='add_listing'),
]