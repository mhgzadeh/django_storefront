from django.db.models import Q
from django.shortcuts import render

from store.models import Product


def say_hello(request):
    # products = Product.objects.all()
    products = Product.objects.filter(~Q(inventory__lt=10) | ~Q(inventory__gt=11))
    return render(request, template_name='hello.html', context={'name': 'Mosh', 'products': list(products)})
