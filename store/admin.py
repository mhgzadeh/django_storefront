from django.contrib import admin

from store.models import Product, Collection, Customer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_price', 'inventory_status')
    list_editable = ('unit_price',)
    list_per_page = 10

    @staticmethod
    @admin.display(ordering='inventory')
    def inventory_status(obj):
        return 'Low' if obj.inventory < 10 else 'Ok'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_product')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable = ('membership',)
    list_per_page = 10
