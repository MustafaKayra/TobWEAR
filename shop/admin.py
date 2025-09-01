from django.contrib import admin
from .models import Product, ProductColor, ProductFeatures, ProductImage, ProductSize


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor)
admin.site.register(ProductFeatures)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
