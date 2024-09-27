from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Bid, Listing, Comment
from auctions.forms import ListingForm, CommentForm, BidForm


def index(request):
    active_listings = Listing.objects.filter(Status=True)
    
    for listing in active_listings:
        listing.check_update_status()

    return render(request, "auctions/index.html", {
        "listings": active_listings
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
            listing.Status = True
            listing.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        form = ListingForm()

    return render(request, 'auctions/newlisting.html', {
        'listing_form' : form
    })

def listing(request, listing_id):

    if listing_id is None:
        return HttpResponse(f"<h1> {listing_id} not found </h1>")

    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing":listing,
        'time_left': listing.time_left()
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
