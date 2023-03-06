from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Agreement, AgreementRequest
from .forms import ListingForm, EditListingForm

# Create your views here.


#Henter hjemmesiden
def home(request): #placeholder
    return render(request, 'homepage/home.html')

#Henter landingpage
def landingpage(request): #placeholder
    return render(request, 'homepage/landingpage.html')

""" def agreementResponse(request, listing_id, agreement_request):
    listing = get_object_or_404(Listing, pk = listing_id)
    

    if request.POST.get('accept_btn'):
        print("accept")

    elif request.POST.get('decline_btn'):
        print("decline") """
    

#Henter en spesifikk annonse, spesifisert med annonse_id
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk = listing_id)
    agreementRequests = listing.agreement_req_listing.all()
    notRequested = True

    if request.POST.get('accept_btn'):
        ag_req_pk = request.POST.get('ag_req_pk_field')
        ag_req = AgreementRequest.objects.get(pk=ag_req_pk)
        print(ag_req)
        print("accept")

    elif request.POST.get('decline_btn'):
        print("decline")

    #Egen siden hvis det er din egen annonse
    if listing.owner == request.user:
        return render(request, 'homepage/my_listing.html', {'listing': listing, 'agreement_requests': agreementRequests})
    

    #Hvis man forespør avtale gjennom knappen
    if request.POST.get('request_btn'):
        agreementRequest = AgreementRequest.objects.create_agreement_request(listing.owner, request.user, listing)
        agreementRequest.save()

    for requests in agreementRequests:
        if requests.loaner == request.user:
            notRequested= False

    return render(request, 'homepage/listing.html', {'listing': listing, 'notRequested': notRequested})
    

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

#Henter en side for å redigere på en spesifikk annonse, spesifisert med annonseid og brukernavn
def edit_listing(request, listing_id):
    queryset = Listing.objects.get(id=listing_id)
    form = EditListingForm(instance=queryset)
    if request.method == 'POST':
        form = EditListingForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            requested_listing = get_object_or_404(Listing, pk = listing_id)
            current_user = request.user
            boolean_same_user = requested_listing.owner == current_user
            context = {'same_user': boolean_same_user, 'listing': requested_listing}
            return render(request, 'homepage/listing.html', context)

    return render(request, 'homepage/listing_edit.html', {'form':form})

#Henter en side for å slette en spesifikk annonse, spesifisert med annonseid og brukernavn
def remove_listing(request, listing_id):
    if request.POST.get('remove_list'):
        listing = get_object_or_404(Listing, pk = listing_id)
        listing.delete()
        return redirect('homepage:listing_overview')
    agreementRequests = listing.agreement_req_listing.all()
    notRequested = True
    for requests in agreementRequests:
        if requests.loaner == request.user:
            notRequested= False
    return render(request, 'homepage/listing.html', {'listing': listing, 'notRequested': notRequested})     