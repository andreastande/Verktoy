# Generated by Django 4.1.5 on 2023-03-02 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_agreement_active_agreement_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Startdato'),
        ),
    ]
