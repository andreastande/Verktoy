from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .forms import ListingForm
from django.db.models import Q
from .models import Listing, Agreement, AgreementRequest
from .forms import ListingForm, EditListingForm
from django.contrib.auth.decorators import login_required

# Create your views here.


#Henter hjemmesiden
def home(request): #placeholder
    return render(request, 'homepage/home.html')

#Henter landingpage
def landingpage(request): #placeholder
    return render(request, 'homepage/landingpage.html')

#Oppretter en avtale, basert på på forespørselen som input
def createAgreement(listing, agreement_request):
        agreement = Agreement.objects.create_agreement_from_request(agreement_request)
        agreement.save()
        agreement_request.delete()
        listing.loaned = True
        listing.save()
    
#Sletter forespørsel om avtale
def declineAgreement(agreement_request):
        agreement_request.delete()

#Henter en spesifikk annonse, spesifisert med annonse_id
@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk = listing_id)
    agreementRequests = listing.agreement_req_listing.all() #forespørsler om å låne annonsen
    notRequested = True #hvorvidt annonsen ikke er forespurt 
    loanedBy = None #blir satt til brukeren som evt har lånt objektet


    #Ved trykk av aksepter-knappen til en av forespørslene på din egen annonse
    if request.POST.get('accept_btn'):
        ag_req_pk = request.POST.get('ag_req_pk_field')
        agreement_request = AgreementRequest.objects.get(pk=ag_req_pk)
        createAgreement(listing, agreement_request)

        #Avslår andre forespørsler knyttet til objektet
        for request in agreementRequests:
            declineAgreement(agreement_request)


    #Ved trykk av avslå-knappen til en av forespørslene på din egen annonse
    elif request.POST.get('decline_btn'):
        ag_req_pk = request.POST.get('ag_req_pk_field')
        agreement_request = AgreementRequest.objects.get(pk=ag_req_pk)
        declineAgreement(agreement_request)

    myListing = False
    #Egen siden hvis det er din egen annonse
    if listing.owner == request.user:
        myListing = True
        if listing.loaned:
            loanedBy = listing.agreement_listing.get(owner=listing.owner).loaner
        context = {'listing': listing, 'notRequested': notRequested, 'loanedBy': loanedBy, 'agreement_requests':agreementRequests}
        return render(request, 'homepage/my_listing.html', context)

    #Hvis man forespør avtale gjennom knappen
    if request.POST.get('request_btn'):
        agreementRequest = AgreementRequest.objects.create_agreement_request(listing.owner, request.user, listing)
        agreementRequest.save()
    
    dropdownList = request.user.list_owner.all()

    if request.POST.get('add_to_fav_btn'):
        active_user = request.user
        chosenUserListName = request.POST.get('userListDD')
        chosenUserList = active_user.list_owner.all().filter(listName=chosenUserListName).first()
        chosenUserList.annonser.add(listing)


    
    dropdownList = request.user.list_owner.all()

    if request.POST.get('add_to_fav_btn'):
        active_user = request.user
        chosenUserListName = request.POST.get('userListDD')
        chosenUserList = active_user.list_owner.all().filter(listName=chosenUserListName).first()
        chosenUserList.annonser.add(listing)


    for requests in agreementRequests:
        if requests.loaner == request.user:
            notRequested= False
    print(myListing)
    context = {'listing': listing, 'notRequested': notRequested, 'loanedBy': loanedBy, 'agreement_requests':agreementRequests, 'myListing':myListing, 'dropdownList':dropdownList}
    return render(request, 'homepage/listing.html', context)
    

def listing_overview(request):
    all_listings = Listing.objects.all()
    q = request.GET.get('q', '')
    qs = request.GET.get('qs', '')
    if qs:
        #Om kategori feltet er valgt
        searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), category=qs)
    else:
        #Om kategori feltet ikke er valgt
        searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q))
    context={'all_listings': all_listings,
             'searchedListings':searchedListings}
    return render(request, 'homepage/listing_overview.html', context)

#Henter side for å opprette ny annonse. Bruker ListingForm definert i forms.py
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
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
            return listing(request, listing_id)

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