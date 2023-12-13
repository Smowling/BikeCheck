from django.contrib import admin

# Register your models here.
from .models import Store, User, Adress


admin.site.register(Store)
admin.site.register(Adress)
admin.site.register(User)
