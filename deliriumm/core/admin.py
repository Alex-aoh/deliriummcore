from django.contrib import admin
from core.models import Event, EventAccount, EventItemType, EventItem, EventSell
from .models import Material
from users.models import RegToken
from users.models import UserCore
from tickets.models import TicketRequest, Ticket, CommentTicketRequest


admin.site.register(UserCore)

admin.site.register(Event)
admin.site.register(TicketRequest)
admin.site.register(Ticket)
admin.site.register(RegToken)
admin.site.register(CommentTicketRequest)
admin.site.register(Material)
admin.site.register(EventAccount)
admin.site.register(EventItemType)
admin.site.register(EventItem)
admin.site.register(EventSell)