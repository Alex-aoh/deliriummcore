# Generated by Django 4.0.4 on 2022-04-27 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_ticketrequest_created_alter_ticketrequest_context_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketrequest',
            name='total',
            field=models.CharField(default='0', max_length=20, verbose_name='Total'),
        ),
    ]
