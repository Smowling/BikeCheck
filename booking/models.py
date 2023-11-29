from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Adress(models.Model):
    city = models.CharField(max_length=80)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    postcode = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.city} {self.postcode}, {self.street} {self.street_number}'

class Contact(models.Model):
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"phone: {self.phone}, email: {self.email}"

    
class User(User):
    contact = models.OneToOneField(
        Contact, on_delete = models.CASCADE,
        null = True
    )
    adress = models.ForeignKey(
        Adress,
        on_delete = models.CASCADE,
        null = True
    )
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Store(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=1000)
    adress = models.ForeignKey(
        Adress,
        on_delete = models.CASCADE,
        null = True
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null = True
    )

    def __str__(self):
        return f'{self.name}'
