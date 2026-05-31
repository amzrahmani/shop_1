# home_module/admin.py
from django.contrib import admin
from .models import Category, ProductBrand, Product, ProductTag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'product_count')
    search_fields = ('title',)

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'تعداد محصولات'


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1
    readonly_fields = ()
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'price', 'best_seller', 'on_sale', 'is_active')
    list_filter = ('category', 'brand', 'best_seller', 'on_sale', 'is_active')
    search_fields = ('title', 'short_description', 'description', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductTagInline]
    ordering = ('-is_active', 'title')


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('caption', 'product')
    search_fields = ('caption', 'product__title')
    list_filter = ('product',)

