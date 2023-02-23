from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .forms import ListingForm

# Create your views here.


#Henter hjemmesiden
def home(request): #placeholder
    return render(request, 'homepage/home.html')

#Henter landingpage
def landingpage(request): #placeholder
    return render(request, 'homepage/landingpage.html')

#Henter en spesifikk annonse, spesifisert med annonse_id
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk = listing_id)
    return render(request, 'homepage/listing.html', {'listing': listing})

def listing_overview(request):
    all_listings = Listing.objects.all()
    return render(request, 'homepage/listing_overview.html', {'all_listings': all_listings})

#Henter side for å opprette ny annonse. Bruker ListingForm definert i forms.py
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            #return render(request, '')
            return redirect('homepage:listing_overview')
    else:
        form = ListingForm()

    return render(request, 'homepage/listing_create.html',{'form':form})
