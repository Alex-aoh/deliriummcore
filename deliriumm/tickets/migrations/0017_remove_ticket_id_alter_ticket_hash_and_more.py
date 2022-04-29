# Generated by Django 4.0.4 on 2022-04-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0016_ticketrequest_staff_asigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='id',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='hash',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='Hash Id'),
        ),
        migrations.AlterField(
            model_name='ticketrequest',
            name='status',
            field=models.CharField(choices=[('PE', 'Pendiente'), ('RE', 'Rechazado'), ('VA', 'Aprobado'), ('AR', 'Archivado')], default='PE', max_length=2),
        ),
    ]
