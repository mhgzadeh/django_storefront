from django.contrib import admin
from django.contrib.admin import register, display
from django.db.models import Count

from store.models import Product, Collection, Customer, Order


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    list_per_page = 10

    @staticmethod
    def products_count(obj):
        return obj.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products')).filter(products_count__gt=0)


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title')
    list_editable = ('unit_price',)
    list_per_page = 10
    list_select_related = ('collection',)

    @staticmethod
    @display(ordering='inventory')
    def inventory_status(obj):
        return 'Low' if obj.inventory < 10 else 'Ok'

    @staticmethod
    @display(ordering='collection')
    def collection_title(obj):
        return obj.collection.title


@register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable = ('membership',)
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'placed_at', 'customer')
    list_per_page = 10
