# Generated by Django 4.0.4 on 2022-04-27 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0013_remove_ticketrequest_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrequest',
            name='staff_asigned',
            field=models.CharField(default='none', max_length=30),
        ),
    ]
