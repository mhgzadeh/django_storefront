from django.contrib import admin, messages
from django.contrib.admin import register, display, action
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from store.models import Product, Collection, Customer, Order, OrderItem, Review


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    list_per_page = 10
    search_fields = ('title',)

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
    actions = ('clear_inventory',)
    autocomplete_fields = ('collection',)
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title')
    list_editable = ('unit_price',)
    list_filter = ('collection', 'last_update', InventoryFilter)
    list_per_page = 10
    list_select_related = ('collection',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    @staticmethod
    @display(ordering='inventory')
    def inventory_status(obj):
        return 'Low' if obj.inventory < 10 else 'Ok'

    @staticmethod
    @display(ordering='collection')
    def collection_title(obj):
        return obj.collection.title

    @action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f"{updated_count} products were successfully updated!", messages.WARNING)


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


# TabularInline vs StackedInline<
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ('product',)
    model = OrderItem
    extra = 1
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ('customer',)
    inlines = (OrderItemInline,)
    list_display = ('id', 'placed_at', 'customer')
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ('product',)

    class Media:
        model = Review
