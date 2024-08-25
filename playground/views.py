# from django.db.models import Q, F
from django.shortcuts import render

from store.models import OrderItem, Product


def say_hello(request):
    # products = Product.objects.all()
    # products = Product.objects.filter(~Q(inventory__lt=10) | ~Q(inventory__gt=11))
    # products = Product.objects.filter(inventory=F('collection__id'))
    ordered_product_ids = OrderItem.objects.values('product_id').distinct()
    products = Product.objects.filter(id__in=ordered_product_ids)
    return render(request, template_name='hello.html', context={'name': 'Mosh', 'products': list(products)})
