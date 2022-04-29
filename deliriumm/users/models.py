from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
 
# User class
class UserCore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
         
        permissions = (
            ("can_view_admin", "To see admin pages"),
            ("can_view_staff", "To see staff pages"),
            ("can_view_rp", "To see rp PAGES"),
        )
    last_ticket_request_see = models.IntegerField(verbose_name="Última Ticket Request visitada", default=0)
# Add other custom permissions according to need.