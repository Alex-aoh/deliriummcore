from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("u/<str:username>", views.public_profile, name="public_profile"),
    path("register/", views.register, name="register")
]
