from django.shortcuts import render

from .models import Store

def index(request):
    return render(request, 'booking/index.html')


def details(request, store_name):
    store = Store.objects.get(name=store_name)
    return render(request, 'booking/details.html', {'store_name': store.name, 'store': store})
