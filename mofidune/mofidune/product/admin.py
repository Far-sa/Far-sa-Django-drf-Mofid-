from django.contrib import admin

from .models import Brand, Category, Product, ProductLine

# Register your models here.


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


# admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductLine)
