# Generated by Django 4.1.6 on 2023-03-12 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='wantToLoan',
            field=models.BooleanField(default=False, verbose_name='Ønskes lånt?'),
        ),
    ]
