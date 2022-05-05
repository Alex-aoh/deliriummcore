import mimetypes
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from tickets.models import Ticket, TicketRequest
from django.db.models import Q

from users.models import UserCore

from .models import Event, Material

# Create your views here.

def download_material(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    path1 = get_object_or_404(Material, pk=pk).file
    # Define text file name
    filename = str(path1)
    # Define the full file path
    filepath = settings.MEDIA_ROOT + filename
    # Open the file for reading content
    with open(filepath, 'rb') as f:
       path = f.read()
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

def delete_material(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.user.has_perm('users.can_view_admin'):
        if os.path.exists(settings.MEDIA_ROOT + str(Material.objects.get(pk=pk).file)):
            os.remove(settings.MEDIA_ROOT + str(Material.objects.get(pk=pk).file))
        Material.objects.get(pk=pk).delete()
        return redirect('core:admin_view')
    return HttpResponseRedirect(reverse("users:login"))


#--------------------------------------------------------------------
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "core/index.html", {
        "event": Event.objects.get(status="VE")
    })
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "core/dashboard.html")
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def events(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "core/events.html", {
        "events": Event.objects.all()
    })
#--------------------------------------------------------------------

# -- STAFF --

#--------------------------------------------------------------------
def staff_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    usercore = get_object_or_404(UserCore, user=request.user)
    if request.user.has_perm('users.can_view_staff') or request.user.has_perm('users.can_view_admin'):
        return render(request, "core/staff/index.html", {
            "tickets_pe": TicketRequest.objects.filter(status="PE"),
            "tickets_re": TicketRequest.objects.filter(status="RE"),
            "tickets_va": TicketRequest.objects.filter(status="VA"),
            "tickets_ar": TicketRequest.objects.filter(status="AR"),
            "last_ticket": usercore.last_ticket_request_see,
        }) 

    else:
        return HttpResponseRedirect(reverse('users:login'))
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def materialCreate(request, event):
    m = Material(description=request.POST['description'], file=request.FILES['material'], event=event)
    return m


def upload_material(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    event = get_object_or_404(Event, status="VE")
    if request.POST:
        try:
            m = materialCreate(request=request, event=event)
        except (BaseException):
            return render(request, "core/admin/upload_material.html",
            {
                "error_message": "¡Ha occurído un error!",
                "event": event
            })
        else:
            m.save()
            return HttpResponseRedirect(reverse("core:admin_view"))
    else:
        return render(request, "core/admin/upload_material.html", {
            "event": event,
        })
#--------------------------------------------------------------------
        





# -- ADMIN --

#--------------------------------------------------------------------
def admin_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    usercore = get_object_or_404(UserCore, user=request.user)
    if request.user.has_perm('users.can_view_admin'):
        return render(request, "core/admin/index.html", {
            "tickets_pe": TicketRequest.objects.filter(status="PE"),
            "tickets_re": TicketRequest.objects.filter(status="RE"),
            "tickets_va": TicketRequest.objects.filter(status="VA"),
            "tickets_ar": TicketRequest.objects.filter(status="AR"),
            "event": Event.objects.get(status="VE"),
            "last_ticket": usercore.last_ticket_request_see,
            "requests_cash": TicketRequest.objects.filter(Q(payment_method="CASH") &  Q(status="VA")),
        }) 

    else:
        return HttpResponseRedirect(reverse('users:login'))
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def rps_cash_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    usercore = get_object_or_404(UserCore, user=request.user)

    # criterion1 = Q(payment_method="CASH") #any query you want
    # criterion2 = Q(FID="id") #any query you want

    

    cashrequests_notpay = {}

    users = User.objects.all()

    for user in users:
        userrequestpay = []
        username = user.username
        ticketrequests = user.ticketrequest_set.all()
        if ticketrequests:
            for ticketrequest in ticketrequests:
                if ticketrequest.payment_method == "CASH":
                    if ticketrequest.cash_pay == False:
                        userrequestpay.append(int(ticketrequest.pk))
            cashrequests_notpay[username] = userrequestpay


    # if keys & values:
    #     for i in range(len(keys)):
    #             cashrequests[keys[i]] = values[i]

            
    #         print(dicts)

    #for users
    ticketsallcash = TicketRequest.objects.filter(payment_method="CASH")
    cashtotal = 0
    ticketnotpay = ticketsallcash.filter(cash_pay=False)
    cashnotpay = 0

    for ticket in ticketsallcash:
        cashtotal = cashtotal + ticket.total
    for ticket in ticketnotpay:
        cashnotpay = cashnotpay + ticket.total
    

    if request.user.has_perm('users.can_view_admin'):
        return render(request, "core/admin/rps_cash.html", {
            "event": Event.objects.get(status="VE"),
            "last_ticket": usercore.last_ticket_request_see,
            "cashrequests": cashrequests_notpay.items(),
            "allrequests": TicketRequest.objects.all(),
            "cashtotal": cashtotal,
            "cashnotpay": cashnotpay,
            "cashpay": cashtotal-cashnotpay,
        }) 

    else:
        return HttpResponseRedirect(reverse('users:login'))