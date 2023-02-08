from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    #path('home', views.home, name='home'), #placeholder
    path('signup', views.signup, name='signup'),

]