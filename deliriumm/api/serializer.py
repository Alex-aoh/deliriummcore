from tickets.models import Ticket
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['hash', 'client', 'use', 'ticketrequest', 'user', 'event', 'price']