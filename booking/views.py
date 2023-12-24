import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Store, User, Bike, Adress
from .forms import AdressForm

def index(request):
    stores = Store.objects.all()
    return render(request, 'booking/index.html', {"stores": stores})


def details(request, store_name):
    store = Store.objects.get(name=store_name)
    details = {'store_name': store.name, 'store': store}
    return render(request, 'booking/details.html', details)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def user_settings(request):
    details = {
        "form": AdressForm(),
    }
    if request.method == "GET":
        adress = Adress.objects.filter(user=request.user)
        if adress:
            details["adress"] = adress
        return render(request, 'booking/settings.html', details )

    form = AdressForm(request.POST)
    if not form.is_valid():
        return render(request, 'booking/settings.html', {"form": form})

    # all good, save redirect
    user = User.objects.get(id = request.user.id)
    auction = form.saveUser(user)
    return HttpResponseRedirect(reverse("settings"))
    
    return render(request, 'booking/settings.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            details = {"message": "Invalid email and/or password."}
            return render(request, "booking/login.html", details)
    else:
        return render(request, "booking/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            details = {"message": "Passwords must match."}
            return render(request, "booking/register.html", details)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            details = {"message": "Email address already taken."}
            return render(request, "booking/register.html", details)
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "booking/register.html")



