from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

client = Client()


class GetMailingsStat(TestCase):
    def setUp(self):
        pass

    def test_get_mailings_stat(self):
        response = client.get(
            reverse('get_common_mailing_stat')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
