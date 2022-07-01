# Generated by Django 4.0.4 on 2022-07-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_lookup', '0003_matchissue_played_with_clubmate'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='brawlclub_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='club_league_playrate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='club_league_teamplay_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='club_league_winrate',
            field=models.FloatField(default=0),
        ),
    ]
