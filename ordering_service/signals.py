from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, **kwargs):
    if instance.status != 'basket' and instance.user.email:
        subject = 'Статус заказа изменен'
        message = f'Заказ {instance.id} был обновлен и имеет новый статус "{instance.status}".'
        from_email = 'noreply@myshop.com'
        recipient_list = [instance.user.email]
        send_mail(subject, message, from_email, recipient_list)