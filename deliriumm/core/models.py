from asyncio import events
from django.db import models

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