# Generated by Django 5.1.1 on 2024-10-01 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_created_at_listing_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time_sent',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
