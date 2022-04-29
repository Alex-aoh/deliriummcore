# Generated by Django 4.0.4 on 2022-04-27 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticketrequest_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketrequest',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Efectivo'), ('CARD', 'Tarjeta'), ('TRANSFER', 'Transferencía'), ('DEPOSIT', 'Deposíto')], default='', max_length=20),
        ),
    ]
