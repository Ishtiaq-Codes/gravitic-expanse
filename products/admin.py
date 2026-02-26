from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'suite_code', 'category', 'price', 'discount_price', 'in_stock', 'featured', 'image_preview', 'created_at']
    list_filter = ['category', 'in_stock', 'featured', 'created_at']
    search_fields = ['name', 'description', 'suite_code']
    list_editable = ['in_stock', 'featured', 'price', 'discount_price']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview_large']
    fieldsets = [
    (None, {
        'fields': ('name', 'slug', 'suite_code', 'category', 'price', 'discount_price', 'image', 'in_stock', 'featured')
    }),
    ('Detailed Info', {
        'fields': ('description', 'image_preview_large'),
        # ❌ remove 'classes': ('collapse',)
    }),
]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px;border-radius:8px;" />', obj.image.url)
        return '—'
    image_preview_large.short_description = 'Image Preview'
