from django import forms
from datetime import timedelta
from auctions.models import Category, Listing, Comment, Bid

class CategoryForm(forms.Form):
    category_name = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        label="Category"
    )

class ListingForm(forms.ModelForm):
    DAYS_CHOICES = [(i, i) for i in range(0, 60)]
    HOURS_CHOICES = [(i, i) for i in range(0, 23)]

    days = forms.ChoiceField(choices=DAYS_CHOICES, label="Days")
    hours = forms.ChoiceField(choices=HOURS_CHOICES, label="Hours")

    class Meta:
        model = Listing
        exclude = ["creator", "Status", "Watchlist", "created_at", "updated_at", "Duration"]
        # Here I just label the fields with akward names deifined in models
        labels = {
            'BidVal': 'Starting Price',
            'ImageUrls': 'Url to image',
            'ProductCat':'Product Category'
        }
        widgets = {
            'BidVal': forms.TextInput(attrs={'placeholder': '€', 'style': 'text-align: right;'})
        }

    def clean(self):
        cleaned_data = super().clean()
        days = int(cleaned_data.get("days", 0))
        hours = int(cleaned_data.get("hours", 0))
        duration = timedelta(days=days, hours=hours)
        cleaned_data["Duration"] = duration
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude =["time_sent", "user", "listing"]
        # Here I just label the fields with akward names deifined in models
        labels = {
            "thecomment" : "Comment"
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["order_time", "username", "listing"]
        labels = {
            'BidValue': 'Amount to Bid',
            'Bid_startime': 'When to start the Bid'
        }
        widgets = {
            'BidValue': forms.TextInput(attrs={'placeholder': 'Higher than Current €', 'style': 'text-align: right;'})
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)  # Get listing object if provided
        super().__init__(*args, **kwargs)

    def clean_BidValue(self):
        bid_value = self.cleaned_data.get('BidValue')

        # Ensure we have a listing object
        if self.listing is None:
            raise forms.ValidationError("Listing is required for bid validation.")

        # Check that the bid value is greater than the current listing bid value
        if bid_value <= self.listing.BidVal:
            raise forms.ValidationError(f"Bid must be greater than the current value of €{self.listing.BidVal}.")

        return bid_value
