from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "full_name", "created_at")
    date_hierarchy = "created_at"
