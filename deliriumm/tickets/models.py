from asyncio.unix_events import _UnixSelectorEventLoop
from numbers import Integral
from sys import maxsize
from tokenize import blank_re
from django.db import models
from django.forms import CharField
from core.models import Event
from django.contrib.auth.models import User

from users.models import UserCore

# Create your models here.


class TicketRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    context = models.CharField(max_length=300, blank=True)
    q_tickets = models.IntegerField(verbose_name="Tickets")
    reference = models.CharField(max_length=150, default="none")
    client = models.CharField(max_length=50, default="none")
    total = models.IntegerField(verbose_name="Total", default="0")
    created = models.DateTimeField(auto_now=True)
    staff_asigned = models.CharField(max_length=30, default="none")

    comprobante = models.FileField(upload_to='uploads/comprobantes/', blank=True)

    PAYMENTS = ( 
        ("CASH", "Efectivo"), 
        ("CARD", "Tarjeta"), 
        ("TRANSFER", "Transferencía"), 
        ("DEPOSIT", "Deposíto"), 
    ) 
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENTS,
        default='CASH',
    )

    cash_pay = models.BooleanField(blank=True, default=False)
    
    STATUS = ( 
        ("PE", "Pendiente"), 
        ("RE", "Rechazado"), 
        ("VA", "Aprobado"), 
        ("AR", "Archivado"), 
    ) 
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='PE',
    )

    

    def __str__(self):
        return "#" + str(self.pk) + " - " + self.user.username + " " + self.status 

class Ticket(models.Model):

    hash = models.CharField(primary_key=True, verbose_name="Hash Id", max_length=200)
    client = models.CharField(max_length=50)
    ticketrequest = models.ForeignKey(TicketRequest, on_delete=models.CASCADE)


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    price = models.IntegerField(verbose_name="Price")

    status_export = models.BooleanField(default=True)

    use = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s" % (self.hash, self.ticketrequest.pk)

class CommentTicketRequest(models.Model):
    ticketrequest = models.ForeignKey(TicketRequest, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)



