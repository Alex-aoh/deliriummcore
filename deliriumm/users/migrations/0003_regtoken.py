# Generated by Django 4.0.4 on 2022-05-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usercore_last_ticket_request_see'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegToken',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=20)),
            ],
        ),
    ]