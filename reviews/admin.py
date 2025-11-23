from django.contrib import admin
from .models import RestaurantReview, ReviewLike, MenuItemReview

@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'title', 'is_verified_purchase', 'likes_count', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('user__email', 'restaurant__name', 'title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'review__title')
    readonly_fields = ('created_at',)

@admin.register(MenuItemReview)
class MenuItemReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'menu_item__name')
    readonly_fields = ('created_at', 'updated_at')
