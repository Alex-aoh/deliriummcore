# Generated by Django 4.0.4 on 2022-05-17 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0029_ticketrequest_cash_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='client',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
