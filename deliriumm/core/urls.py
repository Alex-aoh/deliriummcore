from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("events/", views.events, name="events"),
    path("staff/", views.staff_view, name="staff_view"),
    path("admin/", views.admin_view, name="admin_view"),
    path("material/dowload/<int:pk>", views.download_material, name="dowload_material"),
    path("material/delete/<int:pk>", views.delete_material, name="delete_material"),
    path("material/upload/", views.upload_material, name="upload_material")
]
