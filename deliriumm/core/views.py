from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from tickets.models import TicketRequest

from users.models import UserCore

from .models import Event

# Create your views here.

#--------------------------------------------------------------------
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "core/index.html")
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
        return render(request, "core/events.html", {
            "tickets": TicketRequest.objects.all(),
            "last_ticket": usercore.last_ticket_request_see,
        }) 

    else:
        return HttpResponseRedirect(reverse('users:login'))
#--------------------------------------------------------------------