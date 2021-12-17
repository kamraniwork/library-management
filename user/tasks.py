from django.core.mail import EmailMessage
from kavenegar_gateway.utils import send_sms


def send_email_confirm(email, token, address, inf):
    """
    send email to user for confirm email
    use in Register user
    when signup user, is_active == False and user just confirm your register by email
    then is_active == True
    :param token:
    :param email:
    :return: send to user activate link
    """
    if inf is None:
        body = f"""
        با سلام،
        به منظور تایید ایمیل خود بر روی لینک زیر کلیک نمایید.
        http://localhost:8000/api/auth/{address}/{token}/
        """
    else:
        body = f"""
                با سلام،
                به منظور تایید ایمیل خود بر روی لینک زیر کلیک نمایید.
                http://localhost:8000/api/auth/{address}/{token}/{inf}/
                """
    message = EmailMessage(
        subject='لینک فعال سازی اکانت', body=body, to=[email]
    )
    resp = message.send()


def send_sms_confirm(phone, token, address, inf):
    """
    send sms to user for confirm phone number
    use in Register user
    when signup user, is_active == False and user just confirm your register by sms
    then is_active == True
    :return: send to user activate link
    """
    if inf is None:
        massage = f"""
            با سلام،
            به منظور تایید شماره تلفن خود بر روی لینک زیر کلیک نمایید.
            http://localhost:8000/api/auth/{address}/{token}/
            """
    else:
        massage = f"""
                    با سلام،
                    به منظور تایید شماره تلفن خود بر روی لینک زیر کلیک نمایید.
                    http://localhost:8000/api/auth/{address}/{token}/{inf}/
                    """
    send_sms(phone, massage)


def send_password_forget_token_email(email, token):
    subject = 'فراموشی رمز عبور'
    body = f"""
            با سلام،
            به منظور تایید هویت خودتان جهت تغییر فراموشی رمز عبود، روی لینک زیر کلیک کنید
            http://localhost:8000/api/auth/forget_password/forgot/{token}/
            """
    message = EmailMessage(
        subject=subject, body=body, to=[email]
    )
    resp = message.send()


def send_password_forget_token_sms(phone, token):
    """
    send sms to user for change password phone number
    use in Register user
    :return: send to user activate link
    """
    massage = f"""
                با سلام،
                به منظور تایید هویت خودتان جهت تغییر فراموشی رمز عبود، روی لینک زیر کلیک کنید
                http://localhost:8000/api/auth/forget_password/forgot/{token}/
                """
    send_sms(phone, massage)
