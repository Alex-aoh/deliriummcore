from tickets.models import Ticket, TicketRequest
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['hash', 'client', 'use', 'ticketrequest', 'user', 'event', 'price']

class TicketRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRequest
        fields = ['user', 'event', 'context', 'q_tickets']