from django.shortcuts import render

from store.models import Product


def say_hello(request):
    query_set = Product.objects.get(pk=1)
    return render(request, template_name='hello.html', context={'name': 'Mosh', 'query_set': query_set})
