from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    datetime = models.DateTimeField(verbose_name="Date, Time")
    price = models.IntegerField(verbose_name="Price")

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

