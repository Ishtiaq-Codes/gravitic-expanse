from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'suite_code', 'quantity', 'price', 'get_total']

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'city', 'get_suite_codes','state', 'get_total_quantity', 'total_price', 'status', 'payment_method', 'ordered_at', 'address']
    list_filter = ['status', 'payment_method', 'city', 'ordered_at']
    search_fields = ['name', 'phone', 'email', 'address', 'items__product__suite_code', 'items__suite_code']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['ordered_at', 'updated_at']
    date_hierarchy = 'ordered_at'

    def get_suite_codes(self, obj):
        codes = list(obj.items.values_list('suite_code', flat=True).distinct())
        return ", ".join(filter(None, codes)) or "-"
    get_suite_codes.short_description = 'Suite Codes'

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())
    get_total_quantity.short_description = 'Total Qty'
