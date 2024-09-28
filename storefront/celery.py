import os

from celery import Celery

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='storefront.settings')

celery = Celery('storefront')
celery.config_from_object(obj='django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
