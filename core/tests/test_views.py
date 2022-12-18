import codecs
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Client as ClientModel, Code
from core.serializers import ClientSerializer


# initialize the APIClient app
client = Client()


class GetAllClientsTest(TestCase):
    """ Test module for GET all clients API """

    def setUp(self):
        phones = [
            79000000000,
            79000000001,
            79000000002,
        ]
        codes = [
            900,
            901,
            902,
        ]
        codes_obj = [Code.objects.create(value=c) for c in codes]

        self.clients = []
        for p, c in zip(phones, codes_obj):
            self.clients.append(
                ClientModel.objects.create(phone=p, code=c)
            )

    def test_get_all_clients(self):
        # get API response
        response = client.get(reverse('get_post_clients'))
        # get data from db
        clients = ClientModel.objects.all()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_client(self):
        c, *_ = self.clients
        response = client.get(
            reverse('get_delete_update_client', kwargs={'pk': c.pk}))
        cl = ClientModel.objects.get(pk=c.pk)
        serializer = ClientSerializer(cl)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_client(self):
        response = client.get(
            reverse('get_delete_update_client', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewClientTest(TestCase):
    """ Test module for inserting a new client """

    def setUp(self):

        codes = [
            900,
            901,
            902,
        ]
        codes_obj = [Code.objects.create(value=c) for c in codes]

        self.valid_payload = {
            'phone': 79000000000,
            'code': 900,
            'time_zone': 0,
        }
        self.invalid_payload = {
            'phone': '',
            'code': None,
            'time_zone': 0,
        }

    def test_create_valid_client(self):
        print(Code.objects.all())
        print('_________________')
        response = client.post(
            reverse('get_post_clients'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_client(self):
        response = client.post(
            reverse('get_post_clients'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleClientTest(TestCase):
    """ Test module for updating an existing client record """
    def setUp(self):
        phones = [
            79000000000,
            79000000001,
            79000000002,
        ]
        codes = [
            900,
            901,
            902,
        ]
        codes_obj = [Code.objects.create(value=c) for c in codes]

        self.clients = []
        for p, c in zip(phones, codes_obj):
            self.clients.append(
                ClientModel.objects.create(phone=p, code=c)
            )

        self.valid_payload = {
            'phone': '79000000000',
            'code': 924,
            'tag': None,
            'time_zone': 0,
        }

        self.invalid_payload = {
            'phone': '',
            'code': 924,
            'tag': None,
            'time_zone': 0,
        }

    def test_valid_update_client(self):
        response = client.put(
            reverse('get_delete_update_client', kwargs={'pk': self.clients[0].pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_client(self):
        response = client.put(
            reverse('get_delete_update_client', kwargs={'pk': self.clients[0].pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleClientTest(TestCase):
    """ Test module for deleting an existing client record """
    def setUp(self):
        phones = [
            79000000000,
            79000000001,
            79000000002,
        ]
        codes = [
            900,
            901,
            902,
        ]
        codes_obj = [Code.objects.create(value=c) for c in codes]

        self.clients = []
        for p, c in zip(phones, codes_obj):
            self.clients.append(
                ClientModel.objects.create(phone=p, code=c)
            )

    def test_valid_delete_client(self):
        response = client.delete(
            reverse('get_delete_update_client', kwargs={'pk': self.clients[0].pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_client(self):
        response = client.delete(
            reverse('get_delete_update_client', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
