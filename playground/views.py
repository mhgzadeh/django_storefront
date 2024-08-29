from django.shortcuts import render


def say_hello(request):
    # products = Product.objects.all()
    # products = Product.objects.filter(~Q(inventory__lt=10) | ~Q(inventory__gt=11))
    # products = Product.objects.filter(inventory=F('collection__id'))
    # ordered_product_ids = OrderItem.objects.values('product_id').distinct()
    # products = Product.objects.filter(id__in=ordered_product_ids).order_by('title')
    # products = Product.objects.select_related('collection').prefetch_related('promotions').filter(
    #     promotions__isnull=False)

    # all of them are for reducing the number of the requests to database
    # it will have a meaning when we are hitting the database
    # orders = Order.objects.prefetch_related('items__product').order_by(
    #     '-placed_at')[:5]
    # orders = Order.objects.order_by('-placed_at')[:5]
    # num_orders = Order.objects.all().count()

    # aggregate
    # How many orders do we have?
    # results = Order.objects.all().count()
    # How many units of product 1 have we sold?
    # results = OrderItem.objects.filter(product__id=1).aggregate(sum_quantity=Sum('quantity'))
    # How many orders has customer 1 placed?
    # results = Order.objects.filter(customer_id=1).aggregate(count_order=Count('id'))
    # What is the min, max and average price of the products in collection 3?
    # results = Product.objects.filter(collection_id=3).aggregate(
    #     min_price=Min('price'), max_price=Max('price'), avg_price=Avg('price'))
    return render(request, template_name='hello.html', context={'name': 'Mosh', 'orders': orders})
