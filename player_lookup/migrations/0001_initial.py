# Generated by Django 4.0.4 on 2022-10-07 11:36

from django.db import migrations, models
import django.db.models.deletion
import player_lookup.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brawler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='brawlers/')),
            ],
        ),
        migrations.CreateModel(
            name='BrawlMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='maps/')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('club_tag', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('club_name', models.CharField(max_length=50)),
                ('club_description', models.CharField(blank=True, max_length=200)),
                ('club_type', models.CharField(default='open', max_length=20)),
                ('required_trophies', models.IntegerField(default=0)),
                ('trophies', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('mode', models.CharField(max_length=20)),
                ('battle_type', models.CharField(max_length=20)),
                ('date', models.DateTimeField()),
                ('map_played', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player_lookup.brawlmap')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_tag', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=50)),
                ('trophy_count', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('total_3v3_wins', models.IntegerField(default=0)),
                ('solo_wins', models.IntegerField(default=0)),
                ('duo_wins', models.IntegerField(default=0)),
                ('total_club_war_trophy_count', models.IntegerField(default=0)),
                ('brawlclub_rating', models.FloatField(default=0)),
                ('club_league_winrate', models.FloatField(default=0)),
                ('club_league_playrate', models.FloatField(default=0)),
                ('club_league_teamplay_rate', models.FloatField(default=0)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player_lookup.club', validators=[player_lookup.models.limit_number_of_players])),
            ],
        ),
        migrations.CreateModel(
            name='PlayerHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trophy_count', models.IntegerField(default=0)),
                ('total_club_war_trophy_count', models.IntegerField(default=0)),
                ('brawlclub_rating', models.FloatField(default=0)),
                ('club_league_winrate', models.FloatField(default=0)),
                ('club_league_playrate', models.FloatField(default=0)),
                ('club_league_teamplay_rate', models.FloatField(default=0)),
                ('snapshot_date', models.DateTimeField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_lookup.player')),
            ],
        ),
        migrations.CreateModel(
            name='MatchIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.CharField(choices=[('WIN', 'Win'), ('LOSS', 'Loss'), ('DRAW', 'Draw'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=7)),
                ('trophies_won', models.IntegerField(default=0)),
                ('is_star_player', models.BooleanField(default=False)),
                ('played_with_clubmate', models.BooleanField(default=False)),
                ('brawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_lookup.brawler')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_lookup.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player_lookup.player')),
            ],
        ),
    ]
