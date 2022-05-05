from django.urls import path

from . import views


app_name = "tickets"
urlpatterns = [
    path("", views.index, name="index"),
    path("my_tickets", views.my_tickets, name="my_tickets"),
    path("t/export/<str:hash>", views.temp_ticket_export, name="temp_ticket_export"),
    path("t/requestall/<str:requestid>", views.image_tickets, name="image_tickets"),
    path("t/image/<str:hash>", views.image_ticket, name="image_ticket"),
    path("t/download/<str:tickethash>", views.download_ticket, name="download_ticket"),
    path("r/<int:requestid>", views.request_view, name="request_view"),
    path("r/new", views.create_request_view, name="create_request_view"),
    path("r/new/create", views.new_ticket_request, name="new_ticket_request"),
    path("r/<int:requestid>/delete", views.delete_ticket_request, name="delete_ticket_request"),
    path("a/<int:requestid>", views.admin_request_view, name="admin_request_view"),
    path("a/<int:requestid>/ap", views.aprobar_request, name="aprobar_request"),
    path("a/<int:requestid>/re", views.rechazar_request, name="rechazar_request"),
    path("a/<int:requestid>/ar", views.archivar_request, name="archivar_request"),
    path("a/<int:requestid>/as", views.asignar_request, name="asignar_request"),
    path("a/<int:requestid>/togglecash", views.toggleCash, name="togglecash"),
]
