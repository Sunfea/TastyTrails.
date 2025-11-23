from django.contrib import admin
from .models import SearchQuery, SearchSuggestion

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'search_type', 'ip_address', 'created_at')
    list_filter = ('search_type', 'created_at')
    search_fields = ('query', 'user__email', 'ip_address')
    readonly_fields = ('created_at',)

@admin.register(SearchSuggestion)
class SearchSuggestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'suggestion', 'weight', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('query', 'suggestion')
    readonly_fields = ('created_at', 'updated_at')
