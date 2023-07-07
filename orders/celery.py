import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')
celery_app = Celery('orders')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.autodiscover_tasks()