from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
 
# User class
class UserCore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenum = models.CharField(verbose_name="Numero de Cel", blank=True, max_length=16)
    instagram = models.CharField(verbose_name="Instagram Username", blank=True, max_length=50)

    
    class Meta:
         
        permissions = (
            ("can_view_admin", "To see admin pages"),
            ("can_view_staff", "To see staff pages"),
            ("can_view_rp", "To see rp PAGES"),
        )
    last_ticket_request_see = models.IntegerField(verbose_name="Última Ticket Request visitada", default=0)
# Add other custom permissions according to need.

class RegToken(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    token = models.CharField(max_length=20)

    