# Generated by Django 5.1.1 on 2024-09-10 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_category_bid_listing_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="ImageUrls",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="listing",
            name="startBidVal",
            field=models.FloatField(),
        ),
    ]
