# Generated by Django 4.0.4 on 2022-07-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_lookup', '0006_alter_player_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
