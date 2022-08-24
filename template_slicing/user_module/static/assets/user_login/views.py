from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from .models import User
# Create your views here.
def index(request):
    return render(request, 'user_login/index.html')

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
        password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_login/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "user_login/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_login/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except ValidationError as v:
                return render(request, 'user_login/register.html', {'message': 'Characters must be greater than 3.'})
        except IntegrityError:
            return render(request, "user_login/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'user_login/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "user_login/register.html")