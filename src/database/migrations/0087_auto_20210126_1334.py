# Generated by Django 3.0.7 on 2021-01-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0086_auto_20201116_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagesettings',
            name='featured_events_subtitle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='featured_stats_subtitle',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
