import random
import string
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response


def get_random(length):
    """
    create random for refresh token in users/tokens.py
    :param length: length character for refresh token
    :return: str with Specified Length
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def check_send_email_or_phone_permission(username):
    """
    check How many emails or phone number have been send email or send sms
     It is not possible send email more than 3
    :param username: email or phone
    :return:
    """
    username_count = cache.get('{}{}'.format(settings.EMAIL_SEND_COUNT, username), 0)
    if username_count >= settings.MAX_EMAIL_SEND_COUNT:
        return Response({'access denied': 'you more than 3 time in hours'}, status=403)
    else:
        cache.set('{}{}'.format(settings.EMAIL_SEND_COUNT, username), username_count + 1,
                  timeout=settings.MAX_EMAIL_SEND_TIMEOUT)


def store_token_cache(token, username, time):
    """
    store access_token and refresh_token in redis
    :param token: jwt_token
    :param username: email or phone number
    :param time: in base_test.py ==> MAX_STORE_TOKEN_TIME_OUT= 1 day , MAX_CONFIRM_FORGOT_PASSWORD = 5 minutes,
    MAX_CONFIRM_REGISTER = 5 minutes
    """
    jwt_token = cache.get('{}{}'.format(settings.STORE_TOKEN, username), None)
    if jwt_token is not None:
        cache.delete('{}{}'.format(settings.STORE_TOKEN, username))
    cache.set('{}{}'.format(settings.STORE_TOKEN, username), token, time)


def validate_token(username):
    """
    check that there is jwt_token for user in redis
    :param username: email or phone
    :return: if there is jwt_token in redis return it else return None
    """
    jwt_token = cache.get('{}{}'.format(settings.STORE_TOKEN, username), None)
    if jwt_token is None:
        raise Response({"error": "token expire time"})
    return jwt_token['access']


def check_phone_or_email(inf_string):
    if inf_string.isnumeric():
        return True
    return False
