# Generated by Django 2.2.5 on 2019-10-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0045_vendor_key_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rank',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
