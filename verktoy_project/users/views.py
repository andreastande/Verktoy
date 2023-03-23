from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages
from django.views import generic
from homepage.models import Listing, Agreement
from homepage.models import UserDefinedList
from .forms import MakeFavouritesListForm
from users.models import Profile

# Create your views here.

#https://docs.djangoproject.com/en/4.1/topics/auth/default/#how-to-log-a-user-in
#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

#Henter siden for å registrere ny bruker
def signup(request):
    if request.method == 'POST': #når man sender skjema
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1') #hashet passord
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
        else:
            print("Invalid form")
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = UserCreationForm #når man laster inn login siden først
    return render(request, 'users/signup.html', {'form': form})

#Henter min profil-siden
@login_required
def my_profile(request):
    current_user = request.user
    user_profile = current_user.profile
    activePage = "Settings"
    user_listings = current_user.listing_set.all()
    showSettings = False
    showFavourites = True
    showHistory = False
    heading = 'Mine aktive Annonser'
    if(request.POST.get('update_profile') or request.POST.get('Oppdater')): #Settings
        heading = 'Rediger profil'
        showFavourites = False
        showSettings = True
        showHistory = False
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profilen din ble oppdatert')
            return redirect('users:my_profile')
        else:
            profile_form = ProfileForm(instance=request.user.profile)

        #Returner ting som er relevant for settings
        context = {'history':showHistory,'favourites': showFavourites,'settings':showSettings, 'user': current_user, 'profile': user_profile, 'activePage':activePage,'profile_form': profile_form,'heading':heading}
        return render(request, 'users/my_profile.html', context)
        #update profile
    elif request.POST.get('loaned_out') or request.POST.get('my_loans'):
        #Vise brukers annonser
        listings = []
        if request.POST.get('loaned_out'):
            heading = 'Utlånte annnoser'
            activePage = "LoanedOut"
            for listing in user_listings:
                if listing.loaned:
                    listings.append(listing)
        
        else:
            heading = 'Mine Lån'
            activePage = "MyLoans"
            agreements= Agreement.objects.filter(loaner=request.user)
            for agreement in agreements:
                listings.append(agreement.listing)
            #listings = agreements.objects.agreement_listing.all()

        showSettings = False
        showFavourites = False
        allListings = Listing.objects.all()   
        context = {'history':showHistory,'favourites': showFavourites,'settings':showSettings, 'user': current_user, 'listings': listings, 'profile': user_profile, 'allListings': allListings, 'activePage':activePage,'heading':heading}
        return render(request, 'users/my_profile.html', context)
    
    
    elif (request.POST.get('my_favourites') or request.POST.get('Ny_Liste') ):
        heading = 'Mine Lister'
        activePage = "MyFavourites"
        showHistory = False
        showSettings = False
        mine_favoritter = current_user.list_owner.all()
        form = MakeFavouritesListForm(request.POST)
        if form.is_valid():
            newList = form.save(commit=False)
            newList.owner = current_user
            newList.save()        
        else:
            form = MakeFavouritesListForm()
        
        allListings = Listing.objects.all()
        context = {'history':showHistory,'favourites': showFavourites,'settings':showSettings, 'user': current_user, 'profile': user_profile, 'form':form, 'allListings': allListings,'mine_favoritter':mine_favoritter, 'activePage':activePage,'heading':heading}
        return render(request, 'users/my_profile.html', context)
    elif request.POST.get('historikk_lan') or request.POST.get('historikk_utlan'): 
        showHistory = True
        showFavourites = False
        showSettings = False
        if request.POST.get('historikk_lan'):
            heading = 'Mine tildligere lån'
            activePage = 'historikk_lan'
            history_agreements=Agreement.objects.filter(loaner=current_user).filter(active=False)
        else:
            heading = 'Mine tildligere utlån'
            activePage = 'historikk_utlan'
            history_agreements=Agreement.objects.filter(owner=current_user).filter(active=False)
        context = {'history_agreements':history_agreements,'history':showHistory,'favourites': showFavourites,'settings':showSettings, 'user': current_user, 'profile': user_profile, 'activePage':activePage,'heading':heading}
        return render(request, 'users/my_profile.html', context)

    else: #Default: vise aktive listings
        listings = []
        activePage = "MyListings"
        for listing in user_listings:
            if not listing.loaned:
                listings.append(listing)
        
        showSettings = False
        showFavourites = False
        allListings = Listing.objects.all()   
        context = {'favourites': showFavourites,'settings':showSettings, 'user': current_user, 'listings': listings, 'profile': user_profile, 'allListings': allListings, 'activePage':activePage,'heading':heading}
        return render(request, 'users/my_profile.html', context)
    
    # allListings = Listing.objects.all()
    
    # context = {'settings':showSettings, 'user': current_user, 'listings': listings, 'profile': user_profile, 'mine_favoritter':mine_favoritter, 'form':form, 'allListings': allListings}
    # return render(request, 'users/my_profile.html', context)

@login_required
def profile(request, userstring):
    requested_user = User.objects.get(username = userstring)
    user_listings = requested_user.listing_set.all()
    user_profile = requested_user.profile

    context = {'user': requested_user, 'listings': user_listings, 'profile': user_profile}
    return render(request, 'users/profile.html', context)


#henter siden for å oppdatere profil. Bruker ProfileForm definert i forms.py
@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profilen din ble oppdatert')
            return redirect('users:my_profile')
        
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form}
    return render(request, 'users/update_profile.html', context)

 
#Sletter konto fra databasen
def removeUser(request, userstring):
    current_user = get_object_or_404(User, username = userstring)
    user_listings = Listing.objects.filter(owner = current_user)
    for listings in user_listings:
        listings.delete()
    current_user.delete()
    return redirect('homepage:listing_overview', 'utlån')
    
