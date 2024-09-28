from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Customer
from storefront.settings import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        print(kwargs)
        Customer.objects.create(user=kwargs['instance'])
