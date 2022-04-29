import os
from webbrowser import get
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
import mimetypes

from users.models import UserCore

from .models import TicketRequest, Ticket
from core.models import Event
from hashlib import md5, sha256
import imgkit
from django.conf import settings

# Create your views here.

# -- MAIN --

#--------------------------------------------------------------------
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    usercore = get_object_or_404(UserCore, user=request.user)
    return render(request, "tickets/index.html",{
        "ticketspe": request.user.ticketrequest_set.all().filter(status="PE"),
        "ticketsap": request.user.ticketrequest_set.all().filter(status="VA"),
        "ticketsre": request.user.ticketrequest_set.all().filter(status="RE"),
        "last_ticket": usercore.last_ticket_request_see,

    })
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def my_tickets(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    usercore = get_object_or_404(UserCore, user=request.user)
    return render(request, "tickets/my_tickets.html",{
        "tickets": request.user.ticket_set.all(),
    })
#--------------------------------------------------------------------


#--------------------------------------------------------------------
# -- REQUEST -- 
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def request_view(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    usercore = get_object_or_404(UserCore, user=request.user)
    usercore.last_ticket_request_see = requestid
    usercore.save()

    status_display = ticketrequest.get_status_display()

    if ticketrequest.user == request.user or request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff"):
        return render(request, "tickets/request_view.html", {
            "requestid": requestid,
            "ticketrequest": ticketrequest,
            "status_display": status_display,
            "ticketslist": Ticket.objects.filter(ticketrequest=requestid)
        }) 


#--------------------------------------------------------------------

#--------------------------------------------------------------------
def create_request_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    event_on_sell = get_object_or_404(Event, status="VE")
    return render(request, "tickets/create_request.html", {
        "event": event_on_sell
    })
#--------------------------------------------------------------------



def ticketCreate(request, event, totalp):
    if not request.POST["payment_method"] == "CASH":
        t = TicketRequest(user=request.user, event=event, context=request.POST["context"], 
        q_tickets=int(request.POST["q_tickets"]), reference=request.POST["reference"], 
        client=request.POST["client"], total=totalp, payment_method=request.POST["payment_method"], comprobante=request.FILES["comprobante"])
        return t
    elif request.POST["payment_method"] == "CASH":
        t = TicketRequest(user=request.user, event=event, context=request.POST["context"], 
        q_tickets=int(request.POST["q_tickets"]), reference=request.POST["reference"], 
        client=request.POST["client"], total=totalp, payment_method=request.POST["payment_method"])
        return t
#--------------------------------------------------------------------
def new_ticket_request(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    event = get_object_or_404(Event, status="VE")
    if request.POST["q_tickets"]:
        totalp = int(request.POST["q_tickets"])*event.price
    else:
        totalp=0

    try:
        t = ticketCreate(request=request, event=event, totalp=totalp)
    except (BaseException):
        return render(request, "tickets/create_request.html",
        {
            "error_message": "¡Ha occurído un error!",
            "event": event
        })
    else:
        t.save()
        return HttpResponseRedirect(reverse("tickets:request_view", args=(t.pk,)))
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def delete_ticket_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.POST:
        
        if request.POST.get('yes', False):
            tr = get_object_or_404(TicketRequest, pk=requestid)

            for ticket in tr.ticket_set.all():
                if os.path.exists(settings.MEDIA_ROOT + "/tickets/" + ticket.hash + '.jpg'):
                    os.remove(settings.MEDIA_ROOT + "/tickets/" + ticket.hash +'.jpg')
                if os.path.exists(settings.MEDIA_ROOT + str(tr.comprobante)):
                    os.remove(settings.MEDIA_ROOT + str(tr.comprobante))

            get_object_or_404(TicketRequest, pk=requestid).delete()
            return HttpResponseRedirect(reverse("tickets:index"))
        if request.POST.get('not', False):
            return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))
    return render(request, "tickets/delete_ticket_request.html", {
        "requestid": requestid
    })
#--------------------------------------------------------------------


#--------------------------------------------------------------------
# -- ADMIN REQUESTS -- 
#--------------------------------------------------------------------


#--------------------------------------------------------------------
def admin_request_view(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    usercore = get_object_or_404(UserCore, user=request.user)
    usercore.last_ticket_request_see = requestid
    usercore.save()

    status_display = ticketrequest.get_status_display()

    if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
        return render(request, "tickets/adminrequest/admin_request_view.html", {
            "requestid": requestid,
            "ticketrequest": ticketrequest,
            "status_display": status_display,
            "ticketslist": Ticket.objects.filter(ticketrequest=requestid)
        })
    else:
        return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))
#--------------------------------------------------------------------

#     TICKETS

#--------------------------------------------------------------------
def temp_ticket_export(request, hash):
    status_export = Ticket.objects.get(hash=hash)
    if status_export.status_export == True:
        return render(request, "tickets/ticket_export.html", {
            "hash": hash
        })
    else:
        return reverse("tickets:index")

def image_tickets(request, requestid):
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid) 
    tickets = Ticket.objects.filter(ticketrequest=ticketrequest)
    return render(request, "tickets/image_tickets_request.html", {
        "requestid": requestid,
        "tickets": tickets,
        "ticketrequest": ticketrequest,
    })

def image_ticket(request, hash):
    ticket = get_object_or_404(Ticket, hash=hash)
    return render(request, "tickets/image_tickets.html", {
        "ticket": ticket,
    })

def download_ticket(request, tickethash):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    # Define text file name
    filename = str(tickethash) + ".jpg"
    # Define the full file path
    filepath = settings.MEDIA_ROOT + 'tickets/' + filename
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


def aprobar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    status_display = ticketrequest.get_status_display()

    if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
        ticketrequest.status = "VA"
        ticketrequest.save()


        if ticketrequest.ticket_set.all():
            return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))
        if not ticketrequest.ticket_set.all():
            #NO HAY TICKETS CREADOS
            for t in range(ticketrequest.q_tickets):
                
                hash = hashTicket(event=ticketrequest.event.name, user=request.user.username, request=ticketrequest.pk,id=Ticket.objects.count())
                ticketnew = Ticket(hash=hash, client=ticketrequest.client, ticketrequest=ticketrequest, user=request.user,
                event=ticketrequest.event, price=ticketrequest.event.price, status_export = True)
                ticketnew.save()
                #export html
                #options={'xvfb': ''}
                imgkit.from_url('0.0.0.0:80/core/tickets/t/export/' + hash, settings.MEDIA_ROOT + "tickets/" + hash +'.jpg', options={'xvfb': ''})



            return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))

        
        # return render(request, "tickets/request_view.html", {
        #     "error_message": hash,
        #     "requestid": requestid
        # })
        # return HttpResponseRedirect(reverse("tickets:admin_request_view", args=(requestid,)))
    else:
        return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))

def hashTicket(event, user, request, id):
    request = str(request)
    id = str(id)
    h = md5()
    h.update(event.encode('utf-8'))
    h.update(user.encode('utf-8'))
    h.update(request.encode('utf-8'))
    h.update(id.encode('utf-8'))

    return h.hexdigest()





def rechazar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    status_display = ticketrequest.get_status_display()

    if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
        ticketrequest.status = "RE"
        ticketrequest.save()
        return HttpResponseRedirect(reverse("tickets:admin_request_view", args=(requestid,)))
    else:
        return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))

def archivar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    status_display = ticketrequest.get_status_display()

    if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
        ticketrequest.status = "AR"
        ticketrequest.save()
        return HttpResponseRedirect(reverse("tickets:admin_request_view", args=(requestid,)))
    else:
        return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))

def asignar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if requestid == 0:
        return HttpResponseRedirect(reverse("tickets:index"))
    ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
    status_display = ticketrequest.get_status_display()

    if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
        ticketrequest.staff_asigned = request.user.username
        ticketrequest.save()
        return HttpResponseRedirect(reverse("tickets:admin_request_view", args=(requestid,)))
    else:
        return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))