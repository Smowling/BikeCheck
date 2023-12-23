from django.forms import ModelForm

from .models import Adress

class AdressForm(ModelForm):
    class Meta:
        model = Adress
        # fields = ["title", "description", "category", "picture", "price"]
        exclude = ["user", "store"]

    def saveUser(self, user):
        object = super().save(commit=False)
        object.user = user
        object.save()
        return object

    def saveStore(self, store):
        object = super().save(commit=False)
        object.store = store
        object.save()
        return object
