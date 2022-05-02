import mimetypes
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from tickets.models import TicketRequest

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
        }) 

    else:
        return HttpResponseRedirect(reverse('users:login'))
#--------------------------------------------------------------------