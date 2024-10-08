# Generated by Django 5.1.1 on 2024-09-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_listing_creator"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="mywatchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to="auctions.listing"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="Status",
            field=models.BooleanField(default=False),
        ),
    ]
