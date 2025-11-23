from django.contrib import admin
from .models import Restaurant, Cuisine, RestaurantCuisine, MenuItem, RestaurantHours


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'rating', 'is_active')
    list_filter = ('is_active', 'city', 'rating')
    search_fields = ('name', 'owner__email', 'city')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(RestaurantCuisine)
class RestaurantCuisineAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'cuisine')
    list_filter = ('cuisine',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available')
    list_filter = ('is_available', 'restaurant')
    search_fields = ('name', 'restaurant__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RestaurantHours)
class RestaurantHoursAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'get_day_of_week_display', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('day_of_week', 'is_closed', 'restaurant')
