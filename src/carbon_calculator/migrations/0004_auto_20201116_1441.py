# Generated by Django 3.0.7 on 2020-11-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0086_auto_20201116_1419'),
        ('carbon_calculator', '0003_auto_20200820_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionpoints',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.AddField(
            model_name='actionpoints',
            name='action_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='actionpoints',
            name='action_status',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='group',
            name='member_list',
            field=models.ManyToManyField(blank=True, related_name='group_members', to='database.UserProfile'),
        ),
        migrations.DeleteModel(
            name='CalcUser',
        ),
    ]
