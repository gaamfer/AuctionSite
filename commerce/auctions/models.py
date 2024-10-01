from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.id}: {self.username} at {self.order_time} with a value of {self.BidValue}"
    
    def time_left(self):
        end_time = self.created_at + self.Duration
        current_time = timezone.now()
        time_left = end_time - current_time
        return max(time_left, timedelta(seconds=0))# ensures if time_left is negative, it returns 0
    
    def time_left_str(self):
        time_left = self.time_left()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    
    def check_update_status(self):
        if self.time_left() == timedelta(seconds=0) and self.Status:
            self.Status = False
            self.save()
            

    def __str__(self):
        return (
            f"ID: {self.id} \n"
            f"Created by: {self.creator} \n"
            f"Title: {self.title} \n"
            f"Price: {self.BidVal}, Status: {'Active' if self.Status else 'Inactive'}"
        )
    

class Bid(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE, related_name="last_bid")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    BidValue = models.FloatField()
    order_time = models.DateTimeField(default=datetime.datetime.now)


class Comment(models.Model):
    # src_user, text-based, time_sent, listing_related
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    title=models.CharField(default="Title Here", validators=[MinLengthValidator(5)], max_length=15)
    thecomment=models.CharField(validators=[MinLengthValidator(10)], max_length=500, default="write your comment here")
    time_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} \n {self.title} \n {self.thecomment} \n {self.time_sent}."

