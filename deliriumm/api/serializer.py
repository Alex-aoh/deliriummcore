from tickets.models import Ticket, TicketRequest
from core.models import EventAccount
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['hash', 'client', 'use', 'ticketrequest', 'user', 'event', 'price']

class TicketRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRequest
        fields = ['pk', 'user', 'event', 'context', 'q_tickets']
    
class EventAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAccount
        fields = ['pk', 'username', 'name', 'password']