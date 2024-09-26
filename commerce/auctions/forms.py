from django import forms
from auctions.models import Category, Listing, Comment, Bid

class CategoryForm(forms.Form):
    category_name = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        label="Category"
    )

class ListingForm(forms.ModelForm):
   class Meta:
       model = Listing
       exclude = ["creator", "Status", "Watchlist"]
       # Here I just label the fields with akward names deifined in models
       labels = {
           'BidVal': 'Starting Price',
           'ImageUrls': 'Url to image',
           'ProductCat':'Product Category'
       }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude =["time_sent"]
        # Here I just label the fields with akward names deifined in models
        labels = {
            "thecomment" : "Description"
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["order_time"]
        # Here I just label the fields with akward names deifined in models
        labels = {
            'BidValue': 'Amount to Bid',
            'Bid_startime': 'When to start the Bid'
        }
