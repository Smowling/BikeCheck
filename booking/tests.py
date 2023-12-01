from django.test import TestCase

from django.core.exceptions import ObjectDoesNotExist
from .models import User, Store, Adress, Contact


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


class StoreModelTest(TestCase):
    def test_store_model_exists(self):
        store = Store.objects.count()

        self.assertEqual(store, 0)


    def test_store_model_has_string_representation(self):
        store = Store.objects.create(name="store")

        self.assertEqual(str(store), "store")


    def test_store_contact_exists(self):
        store = Store.objects.create(name="test", details="test details", contact=Contact.objects.create(phone="123123123", email="test@store.pl"))
        contact = Contact.objects.get(id=store.id)

        self.assertTrue(contact is not None)

    def test_store_delete_contact_cascades(self):
        store = Store.objects.create(name="test", details="test details", contact=Contact.objects.create(phone="123123123", email="test@store.pl"))
        store_id = store.id
        store.contact.delete()
        # contact = Contact.objects.filter(id=store_id)

        store = Store.objects.filter(id=store_id)
        contact = Contact.objects.filter(id=store_id)
        self.assertEqual(str(store), 1)


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
