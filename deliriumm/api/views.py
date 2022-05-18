from django.http import HttpResponse
from django.shortcuts import render
from tickets.models import Ticket, TicketRequest
from core.models import EventAccount
from rest_framework import viewsets
from rest_framework import permissions
from .serializer import TicketSerializer, TicketRequestSerializer, EventAccountSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketRequestViewSet(viewsets.ModelViewSet):
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventAccountViewSet(viewsets.ModelViewSet):
    queryset = EventAccount.objects.all()
    serializer_class = EventAccountSerializer
    permission_classes = [permissions.IsAuthenticated]



