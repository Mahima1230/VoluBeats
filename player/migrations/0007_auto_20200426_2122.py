# Generated by Django 3.0.5 on 2020-04-26 15:52

from django.db import migrations, models
import player.models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20200426_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songs',
            name='song_path',
            field=models.FileField(upload_to=player.models.song_path),
        ),
    ]
