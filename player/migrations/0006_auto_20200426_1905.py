# Generated by Django 3.0.5 on 2020-04-26 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20200426_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='songs',
            old_name='song_file',
            new_name='song_path',
        ),
        migrations.RenameField(
            model_name='songs',
            old_name='song_name',
            new_name='song_title',
        ),
    ]