from django.forms import ModelForm

from .models import Address, Bike

class AddressForm(ModelForm):
    class Meta:
        model = Address
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


class BikeForm(ModelForm):
    class Meta:
        model = Bike
        exclude = ["owner"]

    def save(self, user):
        object = super().save(commit=False)
        object.owner = user
        object.save()
        return object

