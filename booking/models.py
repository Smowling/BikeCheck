from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(User):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Store(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.name}'


class Bike(models.Model):
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.CharField(max_length=4)
    sn = models.CharField(max_length=30)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bike_user", primary_key=True)


class Contact(models.Model):
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="contact_store", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_store" ,null=True)

    def __str__(self):
        return f"phone: {self.phone}, email: {self.email}"


class Adress(models.Model):
    city = models.CharField(max_length=80)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    postcode = models.CharField(max_length=5)

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="adress_store", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adress_user" ,null=True)

    def __str__(self):
        return f'{self.city} {self.postcode}, {self.street} {self.street_number}'
