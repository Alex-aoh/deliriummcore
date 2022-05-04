from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import RegToken, UserCore
from django.contrib.auth.models import Group



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


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("core:index"))
    
    if request.POST:
        if request.POST.get('token', False):
            token = get_object_or_404(RegToken, token=request.POST.get('token', False))
            username = token.username
            token.delete()
            form = UserCreationForm()
            return render(request, "users/register.html",{
                'form': form,
                "username": username

        })



        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                if not UserCore.objects.filter(user=user):
                    uc = UserCore(user=user).save()
                my_group = Group.objects.get(name='Rp') 
                my_group.user_set.add(user)
                return redirect('core:index')
    
    else:
        return render(request, "users/token_register.html", {
        })
        


# /users/settings
def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.POST:
        user= request.user
        if request.POST.get('username', False):
            user.username = request.POST['username']
        if request.POST.get('first_name', False):
            user.first_name = request.POST.get('first_name')
        if request.POST.get('last_name', False):   
            request.user.last_name = request.POST['last_name']
        if request.POST.get('email', False):   
            request.user.email = request.POST['email']
        if request.POST.get('phonenum', False):   
            request.user.usercore.phonenum = request.POST['phonenum']
        if request.POST.get('instagram', False):   
            request.user.usercore.instagram = request.POST['instagram']
        request.usercore.save()
        user.save()
        return render(request, "users/settings.html", {
            "user": request.user,
            "message": "¡Información actualizada!",
        })
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
            if not UserCore.objects.filter(user=request.user):
                uc = UserCore(user=request.user).save()
            return HttpResponseRedirect(reverse("core:index"))
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
