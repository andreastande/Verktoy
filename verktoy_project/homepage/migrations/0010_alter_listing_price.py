# Generated by Django 4.1.6 on 2023-03-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_merge_20230306_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Pris'),
        ),
    ]
