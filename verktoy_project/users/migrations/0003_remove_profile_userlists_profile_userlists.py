# Generated by Django 4.1.7 on 2023-03-06 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0011_userdefinedlist'),
        ('users', '0002_profile_userlists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='userLists',
        ),
        migrations.AddField(
            model_name='profile',
            name='userLists',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.userdefinedlist'),
        ),
    ]