# Generated by Django 4.0.8 on 2022-10-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_lookup', '0005_club_has_been_searched_player_has_been_searched'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='number_of_available_tickets',
            field=models.IntegerField(default=0),
        ),
    ]