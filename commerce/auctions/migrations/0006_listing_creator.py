# Generated by Django 5.1.1 on 2024-09-11 10:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_alter_listing_latestbidval"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="creator",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mylistings",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
