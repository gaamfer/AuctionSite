from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

import datetime

# This represents each user of the app
# AbstractUser -> Django built'In User Model
class User(AbstractUser):
    pass
    mywatchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbid")
    BidValue=models.FloatField()
    order_time=models.DateTimeField(default=datetime.datetime.now)
    Bid_startime=models.DateTimeField()

    def __str__(self):
        return f"Order {self.id}: {self.username} at {self.order_time} with a value of {self.BidValue}"

class Listing(models.Model):
    # title, description, startingBidValue, Product_category, URL Image, Status, Watchlist
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mylistings")
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=64)
    BidVal= models.FloatField()
    ProductCat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    ImageUrls = models.ImageField(upload_to='images/', blank=True, null=True)
    Status= models.BooleanField(default=False)
    Duration = models.DurationField()
    Watchlist = models.BooleanField(default=False)
    def __str__(self):
        return (
            f"ID: {self.id} \n"
            f"Created by: {self.creator} \n"
            f"Title: {self.title} \n"
            f"Price: {self.BidVal}, Status: {'Active' if self.Status else 'Inactive'}"
        )


class Comment(models.Model):
    # src_user, text-based, time_sent, listing_related
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    title=models.CharField(default="Title Here", validators=[MinLengthValidator(5)], max_length=30)
    thecomment=models.CharField(validators=[MinLengthValidator(30)], max_length=500, default="write your comment here")
    time_sent = models.DateTimeField()

    def __str__(self):
        return f"{self.id} made at {self.time_sent} on {self.listing}."

