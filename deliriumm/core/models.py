from asyncio import events
from pydoc import describe
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    datetime = models.DateTimeField(verbose_name="Date, Time")
    price = models.IntegerField(verbose_name="Price")
    max_tickets = models.IntegerField(verbose_name="Max Tickets", blank=True, default=0)
    locationmapslink = models.CharField(max_length=300, verbose_name="Google Maps Link", blank=True)

    STATUS = ( 
        ("AN", "Anunciado"), 
        ("VE", "En Venta"), 
        ("TE", "Venta Terminada"), 
        ("AR", "Archivado"), 
    ) 
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='AN',
    )

    def __str__(self):
        return str(self.pk) + " - " + self.name


class Material(models.Model):
    description = models.CharField(max_length=200)
    file = models.FileField(verbose_name="Archivo", upload_to='uploads/materials/', blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    finish = models.BooleanField(default=False)
    description = models.CharField(max_length=300, blank=True)
    file1 = models.FileField(upload_to='uploads/tasks/')
    file2 = models.FileField(upload_to='uploads/tasks/')
    file3 = models.FileField(upload_to='uploads/tasks/')


class EventAccount(models.Model):
    username = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    
class EventSell(models.Model):
    eventaccount = models.ForeignKey(EventAccount, on_delete=models.CASCADE)
    total = models.IntegerField(blank=True, default=0)
    datetime = models.DateTimeField(auto_now=True)


class EventItemType(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=True)
    price = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.pk) + " - " + self.name

class EventItem(models.Model):
    type = models.ForeignKey(EventItemType, on_delete=models.CASCADE)
    eventsell = models.ForeignKey(EventSell, on_delete=models.CASCADE)
    







