from django.db import models
from accounts.models import CustomUser
from restaurants.models import Restaurant, MenuItem, Cuisine


class SearchQuery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    query = models.CharField(max_length=255)
    search_type = models.CharField(max_length=50)  # restaurant, cuisine, menu_item
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} - {self.search_type}"

    class Meta:
        ordering = ['-created_at']


class SearchSuggestion(models.Model):
    query = models.CharField(max_length=255, unique=True)
    suggestion = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)  # Higher weight = more relevant
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.query} -> {self.suggestion}"

    class Meta:
        ordering = ['-weight']
