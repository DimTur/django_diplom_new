from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_status_change_email(current_status, new_status, recipient_email):
    subject = 'Изменение статуса заказа'
    message = f'Статус заказа изменен с {current_status} на {new_status}.'
    from_email = 'noreply@myshop.com'
    recipient_list = [recipient_email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )