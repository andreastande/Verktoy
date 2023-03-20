from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .forms import ListingForm
from django.db.models import Q
from .models import Listing, Agreement, AgreementRequest, Review
from .forms import ListingForm, EditListingForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

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
    reviews = listing.review_set.all()
    alreadyReviewed = False
    totalReviewScore = 0 
    averageReviewScore = 0

    for review in reviews:
        totalReviewScore += review.rating
        if review.user == request.user:
            alreadyReviewed = True
    if (reviews.count() != 0):
        averageReviewScore = totalReviewScore / reviews.count()

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
        context = {'listing': listing, 'notRequested': notRequested, 'loanedBy': loanedBy, 'agreement_requests':agreementRequests, 'reviews':reviews, 'averageReviewScore':averageReviewScore}
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
    context = {'listing': listing, 'notRequested': notRequested, 'loanedBy': loanedBy, 'agreement_requests':agreementRequests, 'myListing':myListing, 'dropdownList':dropdownList, 'reviews':reviews, 'alreadyReviewed':alreadyReviewed, 'averageReviewScore':averageReviewScore}
    return render(request, 'homepage/listing.html', context)

def submit_review(request, listing_id):
    if request.method == "POST":
        try:
            listings= Review.objects.get(user__id = request.user.id, listing__id = listing_id)
            form = ReviewForm(request.POST, instance=listings) 
            form.save()
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                listinga = get_object_or_404(Listing, pk = listing_id)
                data = Review()
                data.title =form.cleaned_data['title'] 
                data.rating =form.cleaned_data['rating'] 
                data.review =form.cleaned_data['review'] 
                data.listing = listinga
                data.user = request.user
                data.save()
        return listing(request, listing_id)

def listing_overview(request, loan):
    if loan=="utlån":
        ctx = {}
        q = request.GET.get('q', '')
        qs = request.GET.get('qs', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        if min_price == '':
            min_price = 0
        if qs and not max_price:
            #Om kategori feltet er valgt og minimum pris skrevet
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), category=qs, price__range=(min_price, 9999), wantToLoan=False)
        elif qs and max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), category=qs, price__range=(min_price, max_price), wantToLoan=False)
        elif not qs and not max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), price__range=(min_price, 9999), wantToLoan=False)
        elif not qs and max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), price__range=(min_price, max_price), wantToLoan=False)
        else:
            #Om kategori feltet ikke er valgt
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), wantToLoan=False)

        ctx["searchedListings"] = searchedListings
        
        does_req_accept_json = request.accepts("application/json")
        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
        
        if is_ajax_request:
            html = render_to_string(
                template_name="listing_overview_loan_partial.html", 
                context={'searchedListings':searchedListings}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)
        
        return render(request, 'homepage/listing_overview_loan.html', context=ctx)
    elif loan=="lånbort":
        ctx = {}
        q = request.GET.get('q', '')
        qs = request.GET.get('qs', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        if min_price == '':
            min_price = 0
        if qs and not max_price:
            #Om kategori feltet er valgt og minimum pris skrevet
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), category=qs, price__range=(min_price, 9999), wantToLoan=True)
        elif qs and max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), category=qs, price__range=(min_price, max_price), wantToLoan=True)
        elif not qs and not max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), price__range=(min_price, 9999), wantToLoan=True)
        elif not qs and max_price:
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), price__range=(min_price, max_price), wantToLoan=True)
        else:
            #Om kategori feltet ikke er valgt
            searchedListings = Listing.objects.filter(Q(title__icontains=q) | Q(location__icontains=q), wantToLoan=True)

        ctx["searchedListings"] = searchedListings
        
        does_req_accept_json = request.accepts("application/json")
        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
        
        if is_ajax_request:
            html = render_to_string(
                template_name="listing_overview_loan_to_partial.html", 
                context={'searchedListings':searchedListings}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)
        
        return render(request, 'homepage/listing_overview_loan_to.html', context=ctx)

#Henter side for å opprette ny annonse. Bruker ListingForm definert i forms.py
@login_required
def add_listing(request, loan):
    if loan=="utlån":
        if request.method == 'POST':
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.owner = request.user
                listing.save()
                #return render(request, '')
                return redirect('homepage:listing_overview', 'utlån')
        else:
            form = ListingForm()

        return render(request, 'homepage/listing_create.html', {'form':form})
    elif loan=="lånbort":
        if request.method == 'POST':
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.owner = request.user
                listing.wantToLoan = True
                listing.save()
                #return render(request, '')
                return redirect('homepage:listing_overview', 'lånbort')
        else:
            form = ListingForm()

        return render(request, 'homepage/listing_create.html',{'form':form})

#Henter en side for å redigere på en spesifikk annonse, spesifisert med annonseid og brukernavn
def edit_listing(request, listing_id):
    queryset = Listing.objects.get(id=listing_id)
    form = EditListingForm(instance=queryset)
    if request.method == 'POST':
        form = EditListingForm(request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            form.save()
            return listing(request, listing_id)

    return render(request, 'homepage/listing_edit.html', {'form':form})

#Henter en side for å slette en spesifikk annonse, spesifisert med annonseid og brukernavn
def remove_listing(request, listing_id):
    if request.POST.get('remove_list'):
        listing = get_object_or_404(Listing, pk = listing_id)
        listing.delete()
        return redirect('homepage:listing_overview', 'utlån')
    agreementRequests = listing.agreement_req_listing.all()
    notRequested = True
    for requests in agreementRequests:
        if requests.loaner == request.user:
            notRequested= False
    return render(request, 'homepage/listing.html', {'listing': listing, 'notRequested': notRequested})     