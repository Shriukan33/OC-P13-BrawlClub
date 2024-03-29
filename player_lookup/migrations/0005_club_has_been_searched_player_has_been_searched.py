# Generated by Django 4.0.8 on 2022-10-17 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_lookup', '0004_alter_player_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='has_been_searched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='has_been_searched',
            field=models.BooleanField(default=False),
        ),
    ]
