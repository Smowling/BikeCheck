from django.contrib import admin

# Register your models here.
from .models import Store, User, Address


admin.site.register(Store)
admin.site.register(Address)
admin.site.register(User)
