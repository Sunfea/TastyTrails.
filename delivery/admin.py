from django.contrib import admin
from .models import DeliveryPerson, Delivery, DeliveryLocation

@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'vehicle_number', 'is_active', 'is_available', 'rating')
    list_filter = ('is_active', 'is_available')
    search_fields = ('user__email', 'vehicle_number', 'license_number')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_person', 'status', 'delivery_fee', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'delivery_person__user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'latitude', 'longitude', 'timestamp')
    readonly_fields = ('timestamp',)
