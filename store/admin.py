from django.contrib import admin
from django.contrib.admin import register, display
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from store.models import Product, Collection, Customer, Order


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    list_per_page = 10

    @staticmethod
    @display(ordering='products_count')
    def products_count(obj):
        url = f"{reverse('admin:store_product_changelist')}?{urlencode({'collection_id': str(obj.id)})}"
        return format_html(f"<a href='{url}'>{obj.products_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products')).filter(products_count__gt=0)


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('low', 'Low')]

    def queryset(self, request, queryset: QuerySet):
        # 'low is the filter value coming from the frontend'
        if self.value() == 'low':
            return queryset.filter(inventory__lt=10)


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title')
    list_editable = ('unit_price',)
    list_filter = ('collection', 'last_update', InventoryFilter)
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
    list_display = ('first_name', 'last_name', 'membership', 'order_count')
    list_editable = ('membership',)
    list_per_page = 10
    search_fields = ('first_name__istartswith', 'last_name__istartswith')

    @staticmethod
    def order_count(obj):
        return obj.order_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('orders'))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'placed_at', 'customer')
    list_per_page = 10
