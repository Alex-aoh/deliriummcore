from django.contrib import admin
from core.models import Event
from users.models import UserCore
from tickets.models import TicketRequest, Ticket, CommentTicketRequest


admin.site.register(UserCore)

admin.site.register(Event)
admin.site.register(TicketRequest)
admin.site.register(Ticket)
