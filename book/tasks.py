from celery import shared_task
from django.core.mail import EmailMessage
from kavenegar_gateway.utils import send_sms
from .models import Issue


@shared_task
def send_email_delay():
    delay_issue = Issue.objects.filter(delay=True)
    for i in delay_issue:
        body = f"""
            با سلام،
            لطفا هرچه سریع تر نسبت به تمدید یا برگرداندن امانت خود اقدام نمایید
            http://localhost:8000/book/issue/{i.pk}/issue_book_email/
            """
        if i.user.email is not None:
            message = EmailMessage(
                subject='تمدید امانتی', body=body, to=[i.user.email]
            )
            resp = message.send()
        else:
            pass


@shared_task
def send_sms_delay():
    delay_issue = Issue.objects.filter(delay=True)
    for i in delay_issue:
        massage = f"""
                با سلام،
                لطفا هرچه سریع تر نسبت به تمدید یا برگرداندن امانت خود اقدام نمایید
                http://localhost:8000/book/issue/{i.pk}/issue_book_email/
                """
        if i.user.phone is not None:
            send_sms(i.user.phone, massage)
        else:
            pass
