# Generated by Django 4.1.5 on 2023-03-04 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0006_alter_agreement_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.listing')),
                ('loaner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreement_req_loaner', to=settings.AUTH_USER_MODEL, verbose_name='Låner')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreement_req_owner', to=settings.AUTH_USER_MODEL, verbose_name='Eier')),
            ],
        ),
    ]