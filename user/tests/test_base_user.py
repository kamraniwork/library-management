from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

User = get_user_model()


class BaseTest(APITestCase):
    """
    Base test case
    """
    client = APIClient

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='mehran', email='mehran@gmail.com',
                                                       password='Mehran1234')

        self.user = User.objects.create_user(username='ali', email='ali@gmail.com', password='Ali123456')
        self.user.is_active = True

        self.user_info = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "Test1234"
        }

    def login_jwt(self, username, password):
        login_data = {
            "username": username,
            "password": password
        }
        token = self.client.post(reverse("auth:login-login-user"), data=login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
