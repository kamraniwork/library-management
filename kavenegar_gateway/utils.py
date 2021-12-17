from kavenegar import *
from django.conf import settings


def send_sms(phone, massage):
    try:
        import json
    except ImportError:
        import simplejson as json

    try:
        # from backend.settings.keys import KAVENEGAR_KEY
        KAVENEGAR_KEY = settings.KAVENEGAR_KEY
    except ImportError:
        print('KAVENEGAR_KEY have not set in settings/keys.py')
    try:
        api = KavenegarAPI(KAVENEGAR_KEY)
        params = {
            'sender': '1000596446',
            'receptor': phone,
            'message': massage
        }
        response = api.sms_send(params)
        return response

    except APIException as e:
        return str(e)

    except HTTPException as e:
        return str(e)

# msg = 'با سلام \n به سامانه سپندار خوش‌آمدید \n\n کد تایید شما: \n 6586'
