from django.test import TestCase
from core.models import Client, Code


class ClientTest(TestCase):
    """ Test module for Client model """
    def setUp(self):
        code = Code.objects.create(value=900)

        Client.objects.create(
            phone=790000000, code=code)

    def test_client_phone_code(self):
        client = Client.objects.get(phone=790000000)
        self.assertEqual(
            client.get_phone(), 790000000)
        self.assertEqual(
            client.get_code(), 900)
        self.assertEqual(type(client.get_code()), int)
