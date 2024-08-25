# from django.db.models import Q, F
from django.shortcuts import render

from store.models import Order


def say_hello(request):
    # products = Product.objects.all()
    # products = Product.objects.filter(~Q(inventory__lt=10) | ~Q(inventory__gt=11))
    # products = Product.objects.filter(inventory=F('collection__id'))
    # ordered_product_ids = OrderItem.objects.values('product_id').distinct()
    # products = Product.objects.filter(id__in=ordered_product_ids).order_by('title')
    # products = Product.objects.select_related('collection').prefetch_related('promotions').filter(
    #     promotions__isnull=False)
    orders = Order.objects.select_related('customer').prefetch_related('items__product').order_by(
        '-placed_at')[:5]
    return render(request, template_name='hello.html', context={'name': 'Mosh', 'orders': list(orders)})
