from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .forms import ListingForm

# Create your views here.

def home(request): #placeholder
    return render(request, 'homepage/home.html')

def listing(request, annonse_id):
    listing = get_object_or_404(Listing, pk = annonse_id)
    return render(request, 'homepage/listing.html', {'listing': listing})

def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        print(request.user)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            #return render(request, '')
            return redirect('homepage:home')
    else:
        form = ListingForm()

    return render(request, 'homepage/listing_create.html',{'form':form})
