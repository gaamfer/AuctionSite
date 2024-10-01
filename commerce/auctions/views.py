from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Bid, Listing, Comment, Category
from auctions.forms import ListingForm, CommentForm, BidForm


def index(request):
    active_listings = Listing.objects.filter(Status=True)
    categories = Category.objects.all()
    
    for listing in active_listings:
        listing.check_update_status()

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": categories
    })

def refined_view(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()

    if not category_id and not search_query:
        return redirect('auctions:index')
    
    listings = Listing.objects.filter(Status=True)

    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            listings = listings.filter(ProductCat=category)
        except Category.DoesNotExist:
            return redirect('auctions:index')
        
    if search_query:
        listings = listings.filter(title__icontains=search_query)
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

#@login_required
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user # setting the signed_In user to the default creator
            listing.Duration = form.cleaned_data["Duration"]
            listing.Status = True
            listing.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        form = ListingForm()

    return render(request, 'auctions/newlisting.html', {
        'form' : form
    })

def listing(request, listing_id):
    if listing_id is None:
        return HttpResponse(f"<h1> {listing_id} not found </h1>")
    
    listing = Listing.objects.get(id=listing_id)
    show_comment_form = request.method == 'POST' and 'show_comment_form' in request.POST
    show_bid_form = request.method == 'POST' and 'show_bid_form' in request.POST

    cform = CommentForm() if show_comment_form else None
    bform = BidForm(listing=listing) if show_bid_form else None

    return render(request, "auctions/listing.html", {
        "listing":listing,
        'time_left': listing.time_left(),
        'cform': cform,
        'show_comment_form': show_comment_form, 
        'bform': bform,
        'show_bid_form': show_bid_form
    })

def mylistings(request, user_id):
    if user_id is None:
        return HttpResponse(f"<h1> {user_id} not found </h1>")

    all_mylistings = Listing.objects.filter(creator=user_id)
    return render(request, "auctions/mylistings.html", {
        "mylistings": all_mylistings
    })

def watchlist_view(request, user_id):
    if user_id is None:
        return HttpResponse(f"<h1> {user_id} not found </h1>")

    user = User.objects.get(id=user_id)
    all_mywatches = user.mywatchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": all_mywatches
    })

def add_to_watchlist(request, listing_id, user_id):
    if request.method == "POST":
        # definig the listing and the user
        listing = Listing.objects.get(id=listing_id)
        theuser = User.objects.get(id=user_id)
        if theuser.mywatchlist.filter(id=listing_id).exists():
            return HttpResponse(f"<h1> {listing.title} already in your watchlist </h1>")
        else:
            theuser.mywatchlist.add(listing)
            listing.Watchlist = True
            listing.save() # just save the listing state
            # i dont need to save theuser because itt is a ManyToManyField
            return HttpResponseRedirect(reverse("auctions:watchlist", kwargs={"user_id": user_id}))

    return HttpResponseRedirect(reverse("auctions:index"))

def remove_from_watchlist(request, listing_id, user_id):
    if request.method == "POST":
        # definig the listing and the user
        listing = Listing.objects.get(id=listing_id)
        theuser = User.objects.get(id=user_id)
        if not theuser.mywatchlist.filter(id=listing_id).exists():
            return HttpResponse(f"<h1> {listing.title} already not in your watchlist </h1>")
        else:
            theuser.mywatchlist.remove(listing)
            listing.Watchlist = False
            listing.save() # just save the listing state
            # i dont need to save theuser because itt is a ManyToManyField
            return HttpResponseRedirect(reverse("auctions:watchlist", kwargs={"user_id": user_id}))

    return HttpResponseRedirect(reverse("auctions:watchlist", kwargs={"user_id": user_id}))


def add_comment(request, listing_id):
    
    listing = Listing.objects.get(id=listing_id)

    if request.method == 'POST':
        cform = CommentForm(request.POST)
        if cform.is_valid():
            comment = cform.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
            return redirect('auctions:listing', listing_id=listing.id)
    
    return redirect('auctions:listing', listing_id=listing.id)

def new_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.method == 'POST':
        bform = BidForm(request.POST, listing=listing)
        if bform.is_valid():
            bid = bform.save(commit=False)
            bid.username = request.user
            bid.listing = listing
            bid.save()
            listing.BidVal = bid.BidValue
            listing.save()
            return redirect('auctions:listing', listing_id=listing.id)
        
    return redirect('auctions:listing', listing_id=listing.id)