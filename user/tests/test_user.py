from .test_base_user import BaseTest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class Account(BaseTest):

    def test_register_user_by_email(self):
        """ Test for register user with email and check is_active field """

        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info)

        user = User.objects.get(username=self.user_info['username'])
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_invalid_email(self):
        """ Test dont register user if email is invalid """

        self.user_info['email'] = 'test'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info)

        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_custom_email(self):
        """ Test register user if email is uppercase """

        self.user_info['email'] = 'TEST@GMAIL.com'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info)

        user = User.objects.get(username='test2')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

