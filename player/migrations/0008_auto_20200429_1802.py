# Generated by Django 3.0.5 on 2020-04-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20200426_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='id',
        ),
        migrations.AlterField(
            model_name='artist',
            name='artist',
            field=models.CharField(max_length=70, primary_key=True, serialize=False),
        ),
    ]