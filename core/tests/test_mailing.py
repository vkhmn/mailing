import json
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from core.models import Mailing, Filter, Code
from django.test import Client, TestCase

from core.serializers import MailingSerializer

client = Client()


class TestMailingView(TestCase):
    def setUp(self):
        code, _ = Code.objects.get_or_create(value=900)
        f = Filter.objects.create(
            code=code,
        )
        self.m = Mailing.objects.create(
            time_start=datetime.strptime('20-12-2022 20:00', '%d-%m-%Y %H:%M'),
            filter=f,
            message_text='Hello world',
            time_end=datetime.strptime('21-12-2022 20:00', '%d-%m-%Y %H:%M'),
        )

    #    qs = Mailing.objects.all()
    #    print(qs, 'dff')

    def test_mailing_create(self):
        qs = Mailing.objects.all()
        self.assertEqual(list(qs)[0].message_text, 'Hello world')

    def test_get_single_mailing(self):
        response = client.get(
            reverse('get_delete_update_mailing', kwargs={'pk': self.m.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mailings(self):
        response = client.get(
            reverse('get_post_mailing')
        )
        mailing = Mailing.objects.all()
        serialize = MailingSerializer(mailing, many=True)

        self.assertEqual(response.data, serialize.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewMailingTest(TestCase):
    """ Test module for inserting a new mailing """

    def setUp(self):
        self.valid_payload = {
            'time_start': '20-12-2022 20:00',
            'filter': {
                'code': 900,
                'tag': None,
            },
            'message_text': 'Hello world',
            'time_end': '21-12-2022 20:00',
        }
        self.invalid_payload = {
            'time_start': '20-12-2022 20:00',
            'filter': {
                'code': None,
                'tag': None,
            },
            'message_text': 'Hello world',
            'time_end': '21-12-2022 20:00',
        }

    def test_create_valid_mailing(self):
        response = client.post(
            reverse('get_post_mailing'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_client(self):
        response = client.post(
            reverse('get_post_mailing'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleMailingTest(TestCase):
    """ Test module for updating an existing client record """
    def setUp(self):

        code, _ = Code.objects.get_or_create(value=900)
        f = Filter.objects.create(
            code=code,
        )
        self.m = Mailing.objects.create(
            time_start=datetime.strptime('20-12-2022 20:00', '%d-%m-%Y %H:%M'),
            filter=f,
            message_text='Hello world',
            time_end=datetime.strptime('21-12-2022 20:00', '%d-%m-%Y %H:%M'),
        )

        self.valid_payload = {
            'time_start': '20-12-2022 20:00',
            'filter': {
                'code': 901,
                'tag': None,
            },
            'message_text': 'Hello world',
            'time_end': '21-12-2022 20:00',
        }
        self.invalid_payload = {
            'time_start': '20-12-2022 20:00',
            'filter': {
                'code': None,
                'tag': None,
            },
            'message_text': 'Hello world',
            'time_end': '21-12-2022 20:00',
        }

    def test_valid_update_mailing(self):
        response = client.put(
            reverse('get_delete_update_mailing', kwargs={'pk': self.m.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_mailing(self):
        response = client.put(
            reverse('get_delete_update_mailing', kwargs={'pk': self.m.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleMailingTest(TestCase):
    """ Test module for deleting an existing client record """
    def setUp(self):
        code, _ = Code.objects.get_or_create(value=900)
        f = Filter.objects.create(
            code=code,
        )
        self.m = Mailing.objects.create(
            time_start=datetime.strptime('20-12-2022 20:00', '%d-%m-%Y %H:%M'),
            filter=f,
            message_text='Hello world',
            time_end=datetime.strptime('21-12-2022 20:00', '%d-%m-%Y %H:%M'),
        )

    def test_valid_delete_mailing(self):
        response = client.delete(
            reverse('get_delete_update_mailing', kwargs={'pk': self.m.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_mailing(self):
        response = client.delete(
            reverse('get_delete_update_mailing', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
