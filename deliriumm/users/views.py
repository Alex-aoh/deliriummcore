from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



# Create your views here.

# /users/     REDIRECT TO LOGIN OR CORE HOME
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return HttpResponseRedirect(reverse("users:profile"))


# /users/profile  IFNOT LOGIN REDIRECT TO LOGIN // RENDER USER.HTML (PROFILE PAGE)
def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/profile.html", {
        "user": request.user
    })

# /users/u/<username> IFNOT LOGIN REDIRECTO TO LOGIN // GET <USERNAME> IF NOT 404 //
# 
# USERP = REQUEST.USER --> PROFILE /
# IFNOT RENDER PUBLIC PROFILE

def public_profile(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    prof_user = get_object_or_404(User, username=username)
    if prof_user == request.user:
        return HttpResponseRedirect(reverse('users:profile'))
    return render(request, "users/public_profile.html", {
        "user": request.user,
        "profile_user": prof_user
    })



# /users/settings
def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/settings.html", {
        "user": request.user
    })


# /users/login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:profile"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "users/login.html")


# /users/logout
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })
