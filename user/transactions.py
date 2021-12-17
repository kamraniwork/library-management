from django.contrib.auth import get_user_model
from django.db import transaction


@transaction.atomic
def register_user_with_email_or_phone_and_password(username=None, email=None, phone=None, password=None):
    user = get_user_model().objects.create_user(username=username, email=email, phone=phone, password=password)
    return user


@transaction.atomic
def change_user_password(user, password):
    user.set_password(password)
    user.save()
