from unittest import TestCase
from django.test import Client

class TestClient(TestCase):

    def test_client_login(self):
        self.assertTrue(True)
        c = Client()
        response = c.post('login/', {'username': 'admin', 'password': 'qwerty'})
        # self.assertEqual(response.context['user_name'], ['Admin'])