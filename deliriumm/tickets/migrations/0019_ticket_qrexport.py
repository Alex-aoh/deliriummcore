# Generated by Django 4.0.4 on 2022-04-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0018_ticket_status_export'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='qrexport',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Boleto'),
        ),
    ]
