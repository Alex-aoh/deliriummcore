# Generated by Django 4.0.4 on 2022-04-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_alter_ticketrequest_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketrequest',
            name='total',
            field=models.IntegerField(default='0', max_length=20, verbose_name='Total'),
        ),
    ]
