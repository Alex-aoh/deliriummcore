# Generated by Django 4.0.4 on 2022-05-02 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0027_alter_ticketrequest_comprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='use',
            field=models.BooleanField(default=False),
        ),
    ]
