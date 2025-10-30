from django.contrib import admin

from .models import CartItem, Order, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "updated_at")
    search_fields = ("user__username", "product__name")
    list_select_related = ("user", "product")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_type", "created_at")
    list_filter = ("payment_type", "created_at")
    search_fields = ("user__username", "full_name")
    inlines = [OrderItemInline]
