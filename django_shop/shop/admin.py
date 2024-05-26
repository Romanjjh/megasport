from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Review


class OrderReviewInline(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'available', 'get_html_photo']
    list_filter = ['available']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    inlines = [OrderReviewInline]

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(
                f"<img src='{object.image.url}' width=65>")

    get_html_photo.short_description = ' '
