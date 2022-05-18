# Generated by Django 4.0.4 on 2022-05-17 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EventItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventSell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(blank=True, default=0)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('eventaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.eventaccount')),
            ],
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventsell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.eventsell')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.eventitemtype')),
            ],
        ),
    ]
