from django.test import TestCase, Client

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Store, Adress, Contact, Bike


class ContactModelTest(TestCase):
    def test_contact_model_exists(self):
        contact = Contact.objects.count()
        self.assertEqual(contact, 0)

    def test_contact_has_string_representation(self):
        contact = Contact.objects.create(phone="123123123", email="asd@asd.pl")
        self.assertEqual(str(contact), "phone: 123123123, email: asd@asd.pl")


class UserModelTest(TestCase):
    def test_user_model_exists(self):
        users = User.objects.count()
        self.assertEqual(users, 0)

    def test_user_has_string_representation(self):
        user = User.objects.create(username="test", first_name="test", last_name="test")
        self.assertEqual(str(user), "test test")

    def test_user_contact_exists(self):
        user = User.objects.create(username="test", first_name="test", last_name="test")
        contact = Contact.objects.create(phone="123123123", email="user@user.pl", user=user)
        contact = Contact.objects.get(id=user.id)
        self.assertTrue(contact is not None)

    def test_user_delete_contact_cascades(self):
        user = User.objects.create(username="test", first_name="test", last_name="test")
        contact = Contact.objects.create(phone="123123123", email="user@user.pl", user=user)
        user.delete()
        contact = Contact.objects.all().count()
        self.assertEqual(contact, 0)
        

class StoreModelTest(TestCase):
    def test_store_model_exists(self):
        store = Store.objects.count()
        self.assertEqual(store, 0)


    def test_store_model_has_string_representation(self):
        store = Store.objects.create(name="store")
        self.assertEqual(str(store), "store")


    def test_store_contact_exists(self):
        store = Store.objects.create(name="test", details="test details")
        contact = Contact.objects.create(phone="123123123", email="test@asd.pl", store=store)
        contact = Contact.objects.get(id=store.id)
        self.assertTrue(contact is not None)

    def test_store_delete_contact_cascades(self):
        store = Store.objects.create(name="test", details="test details")
        contact = Contact.objects.create(phone="123123123", email="test@asd.pl", store=store)
        contact2 = Contact.objects.create(phone="123123123", email="test@asd.pl", store=store)

        self.assertTrue(store is not None)
        count = Contact.objects.all().count()
        self.assertEqual(count, 2)
        store.delete()
        store = Store.objects.all().count()
        contact = Contact.objects.all().count()
        self.assertEqual(store, 0)
        self.assertEqual(contact, 0)
        


class AdressModelTest(TestCase):
    def test_adress_model_exists(self):
        adress = Adress.objects.count()
        self.assertEqual(adress, 0)


class BookingIndexPageTest(TestCase):
    def test_booking_index_page_returns_200_response(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'booking/index.html')
        self.assertEqual(response.status_code, 200)
        
    def test_booking_index_page_has_stores(self):
        response = self.client.get('/')
        

class StoreDetailsPageTest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(name='bikecheck', details='bikecheck details')
    

    def test_store_details_page_returns_200_response(self):
        response = self.client.get(f'/store/{self.store.name}/')
        self.assertTemplateUsed(response, 'booking/details.html')
        self.assertEqual(response.status_code, 200)


    def test_store_details_page_has_store_details(self):
        response = self.client.get(f'/store/{self.store.name}/')
        self.assertContains(response, self.store.name)
        self.assertContains(response, self.store.details)


class BikeModelTest(TestCase):
    def test_bike_model_exists(self):
        bike = Bike.objects.count()
        self.assertEqual(bike, 0)

    def test_bike_model_create(self):
        user = User.objects.create(username="testUser")
        bike = Bike.objects.create(brand="Santa", model="hightower", year="2020", owner=user)
        count = Bike.objects.all().count()
        self.assertEqual(count, 1)

    def test_bike_model_delete_cascades(self):
        user = User.objects.create(username="testUser")
        bike = Bike.objects.create(brand="Santa", model="hightower", year="2020", owner=user)
        user.delete()
        count = Bike.objects.all().count()
        self.assertEqual(count, 0)


class LoginPageTest(TestCase):
    def setUp(self):
        self.credentials = {
                    'username': 'testuser',
                    'password': 'secret'}
        User.objects.create_user(**self.credentials)
        
    def test_login_page_returns_correct_response(self):
        response = self.client.get(f'/login/')
        self.assertTemplateUsed(response, 'booking/login.html')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page_contains_form(self):
        response = self.client.get(f'/login/')
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_form(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_active)
        self.assertRedirects(response, reverse("index"), status_code=302, target_status_code=200)
      

class RegisterPageTest(TestCase):
    
    def test_register_page_returns_correct_response(self):
        response = self.client.get(f'/register/')
        self.assertTemplateUsed(response, 'booking/register.html')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page_contains_form(self):
        response = self.client.get(f'/register/')
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
