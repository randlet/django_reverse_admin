from copy import copy
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from polls.models import Address
from polls.models import Person
import polls.tests.config as test_config


class AddressAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(**test_config.ADMIN_USER)

    def test_add_address(self):
        self.assertEquals(0, Address.objects.count())

        client = Client()
        client.login(**test_config.ADMIN_USER)
        change_url = reverse('admin:polls_address_add')
        data = test_config.ADDRESS
        client.post(change_url, data)
        self.assertEquals(1, Address.objects.count())
        address = Address.objects.all()[0]

        # Edit the address now
        change_url = reverse('admin:polls_address_change', args=(address.id,))
        data = test_config.ADDRESS_2
        client.post(change_url, data)
        self.assertEquals(1, Address.objects.count(), 'there is still 1 address')
        address = Address.objects.all()[0]
        self.assertEquals(address.street_2, test_config.ADDRESS_2['street_2'], 'but the address has changed')


class PersonAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(**test_config.ADMIN_USER)

    def test_add_person_with_address(self):
        self.assertEquals(0, Person.objects.count())

        client = Client()
        client.login(**test_config.ADMIN_USER)
        change_url = reverse('admin:polls_person_add')
        client.post(change_url, test_config.PERSON_WITH_ADDRESS)
        self.assertEquals(1, Person.objects.count())
        person = Person.objects.all()[0]

        # Edit the persons address now
        change_url = reverse('admin:polls_person_change', args=(person.id,))
        test_config.PERSON_WITH_ADDRESS_2['form-0-id'] = person.home_addr.id
        client.post(change_url, test_config.PERSON_WITH_ADDRESS_2)
        data = copy(test_config.PERSON_WITH_ADDRESS_2)
        data['form-INITIAL_FORMS'] = 0
        data['form-0-id'] = ''
        client.post(change_url, data)
        self.assertEquals(1, Person.objects.count())
        self.assertEquals(1, Address.objects.count())

        person = Person.objects.all()[0]
        self.assertEquals(person.home_addr.state, test_config.PERSON_WITH_ADDRESS_2['form-0-state'], 'but the address has changed')
