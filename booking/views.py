import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Store, User, Bike, Address
from .forms import AddressForm, BikeForm

def index(request):
    stores = Store.objects.all()
    return render(request, 'booking/index.html', {"stores": stores})


def details(request, store_name):
    store = Store.objects.get(name=store_name)
    context = {'store_name': store.name, 'store': store}
    return render(request, 'booking/details.html', context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def add_address(request):
    context = {
        "addressform": AddressForm(request.POST or None),
    }
    if request.method == "GET":
        adress = Address.objects.filter(user = request.user)
        if adress:
            context["adress"] = adress
        return render(request, 'booking/account.html', context )

    form = AddressForm(request.POST)
    if not form.is_valid():
        return render(request, 'booking/account.html', {"addressform": form})

    user = User.objects.get(id = request.user.id)
    adress = form.saveUser(user)
    return HttpResponseRedirect(reverse("account"))


@login_required
def add_bike(request):
    context = {
        "bikeform": BikeForm(request.POST or None),
            }
    if request.method == "GET":
        bike = Bike.objects.filter(owner = request.user)
        if bike:
            context["bike"] = bike
        return render(request, 'booking/account.html', context)
    form = BikeForm(request.POST)
    if not form.is_valid():
        return render(request, 'booking/account.html', {"bikeform": form})

    user = User.objects.get(id = request.user.id)
    bike = form.save(user)
    return HttpResponseRedirect(reverse("account"))


@login_required
def edit_address(request, id=None, template = 'booking/account.html'):
    if id:
        address = get_object_or_404(Address, pk=id)
        if address.user.id != request.user.id:
            return HttpResponseForbidden()

    form = AddressForm(request.POST or None, instance=address)
    if request.POST and form.is_valid():
        form.saveUser(request.user)
        return redirect(reverse('account'))

    context = {}
    context["addressform"] = form
    return render(request, template, context)


@login_required
def edit_bike(request, id=None, template = 'booking/account.html'):
    if id:
        bike = get_object_or_404(Bike, pk=id)
        if bike.owner.id != request.user.id:
            return HttpResponseForbidden()
    form = BikeForm(request.POST or None, instance=bike)
    if request.POST and form.is_valid():
        form.save(request.user)
        return redirect(reverse('account'))
    context = {}
    context["bikeform"] = form
    return render(request, template, context)


@login_required
def account(request):
    context = {}
    user = User.objects.get(id = request.user.id)
    adresses = Address.objects.filter(user = user)
    context['addresses'] = adresses
    bikes = Bike.objects.filter(owner = user)
    context['bikes'] = bikes

    return render(request, 'booking/account.html', context)


@login_required
def user_context_add_address(request):
    context = {}
    context["form"] = AddressForm()
    user = User.objects.get(id = request.user.id)
    
    return render(request, 'booking/account.html', context)


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
            context = {"message": "Invalid email and/or password."}
            return render(request, "booking/login.html", context)
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
            context = {"message": "Passwords must match."}
            return render(request, "booking/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            context = {"message": "Email address already taken."}
            return render(request, "booking/register.html", context)
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "booking/register.html")


@login_required
def bikedelete(request, id):
    bike = get_object_or_404(Bike, pk=id)
    if bike.owner.id != request.user.id:
        return HttpResponseForbidden()
    bike.delete()
    return HttpResponseRedirect(reverse('account'))


@login_required
def addressdelete(request, id):
    address = get_object_or_404(Address, pk=id)
    if address.user.id != request.user.id:
        return HttpResponseForbidden()
    address.delete()
    return HttpResponseRedirect(reverse('account'))

