from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Varsayılan olarak gösterilecek ek satır sayısı

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
