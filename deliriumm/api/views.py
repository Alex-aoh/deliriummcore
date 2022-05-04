from django.http import HttpResponse
from django.shortcuts import render
from tickets.models import Ticket, TicketRequest
from rest_framework import viewsets
from rest_framework import permissions
from .serializer import TicketSerializer, TicketRequestSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketRequestViewSet(viewsets.ModelViewSet):
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer
    permission_classes = [permissions.IsAuthenticated]



