# Generated by Django 4.0.4 on 2022-05-18 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_eventaccount_eventitemtype_eventsell_eventitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventaccount',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='eventaccount',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
