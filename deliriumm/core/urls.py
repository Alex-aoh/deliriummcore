from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("events/", views.events, name="events"),
    path("staff/", views.staff_view, name="staff_view"),
    path("admin/", views.admin_view, name="admin_view"),
]
