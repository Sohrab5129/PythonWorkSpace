from django.contrib import admin

# Register your models here.

from product.models import Product, Quantity


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img', 'desc', 'price', 'offer')


class QuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'qty', 'soldQty')


admin.site.register(Product, ProductAdmin)
admin.site.register(Quantity, QuantityAdmin)
