from extension.base_test import BaseTest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.conf import settings
from django.core import mail
from django.core.cache import cache

User = get_user_model()


class Account(BaseTest):

    def test_register_user_by_email(self):
        """ Test for register user with email and check is_active field """

        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        user = User.objects.get(username=self.user_info_email['username'])
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(cache.get(f"CACHE_STORE_TOKEN_{self.user_info_email['username']}")['username'],
                         self.user_info_email['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_error_user_by_email(self):
        """ Test error for register user with email when username is repetitious """

        self.user_info_email['username'] = 'ali'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_invalid_email(self):
        """ Test dont register user if email is invalid """

        self.user_info_email['email'] = 'test'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_custom_email(self):
        """ Test register user if email is uppercase """

        self.user_info_email['email'] = 'TEST@GMAIL.com'
        response = self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)

        user = User.objects.get(username='test2')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_by_phone(self):
        """ Test for register user with phone number and check is_active field """

        response = self.client.post(reverse("auth:register-register-phone"), data=self.user_info_phone)

        user = User.objects.get(username=self.user_info_phone['username'])
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(cache.get(f"CACHE_STORE_TOKEN_{self.user_info_phone['username']}")['username'],
                         self.user_info_phone['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_invalid_phone(self):
        """ Test dont register user if phone number is invalid """

        self.user_info_phone['phone'] = '09863827621'
        response = self.client.post(reverse("auth:register-register-phone"), data=self.user_info_phone)

        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_register_error(self):
        """ Test dont confirm user when token is invalid """

        self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)
        response = self.client.get(reverse("auth:confirm-confirm-register", args=[
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQzMzkyODk4LCJpYXQiOjE2NDMzOTI1OTgsImp0aSI6IjQ5NDg1MjEwNGQ1MzRmNzM4YmI2Njg5MzA2kjxyODdhIiwidXNlcl9pZCI6OX0.su7em94PLTg3Kj-NQBtcPguaaihxoinkfxrWejclwg8o']))

        user = User.objects.get(username=self.user_info_email['username'])

        self.assertFalse(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_user(self):
        """ Test dont confirm user if everything is correct """

        self.client.post(reverse("auth:register-register-email"), data=self.user_info_email)
        response = self.client.get(reverse("auth:confirm-confirm-register", args=[
            cache.get(f"CACHE_STORE_TOKEN_{self.user_info_email['username']}")['access']]))

        user = User.objects.get(username=self.user_info_email['username'])
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
