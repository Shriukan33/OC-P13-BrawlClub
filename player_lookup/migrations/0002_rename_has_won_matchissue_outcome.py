# Generated by Django 4.0.4 on 2022-05-15 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player_lookup', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchissue',
            old_name='has_won',
            new_name='outcome',
        ),
    ]
