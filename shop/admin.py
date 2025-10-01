from django.contrib import admin
from .models import Product, ProductColor, ProductFeatures, ProductImage, ProductSize, ProductCategory, OrderItem, ShoppingCard, OrderCard, Contact


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductColor)
admin.site.register(ProductFeatures)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(ProductCategory)
admin.site.register(OrderItem)
admin.site.register(ShoppingCard)
admin.site.register(Contact)

class OrderCardAdmin(admin.ModelAdmin):
    list_display = ("shoppingcard", "date", "complete")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.complete:
            shoppingcard = obj.shoppingcard
            obj.delete()
            shoppingcard.delete()
admin.site.register(OrderCard,OrderCardAdmin)
