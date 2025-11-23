from django.shortcuts import render
from django.db.models import Q
from restaurants.models import Restaurant, MenuItem, Cuisine
from .models import SearchQuery, SearchSuggestion


def search(request):
    """Handle search requests"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'restaurant')
    
    # Save search query
    if query:
        SearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=query,
            search_type=search_type,
            ip_address=request.META.get('REMOTE_ADDR')
        )
    
    results = []
    if query:
        if search_type == 'restaurant':
            results = Restaurant.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(city__icontains=query)
            ).distinct()
        elif search_type == 'cuisine':
            results = Cuisine.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            ).distinct()
        elif search_type == 'menu_item':
            results = MenuItem.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            ).select_related('restaurant').distinct()
    
    # Get search suggestions
    suggestions = SearchSuggestion.objects.filter(is_active=True)[:10]
    
    context = {
        'query': query,
        'search_type': search_type,
        'results': results,
        'suggestions': suggestions,
    }
    return render(request, 'search/search_results.html', context)


def search_suggestions(request):
    """Return search suggestions as JSON"""
    from django.http import JsonResponse
    
    query = request.GET.get('q', '')
    if query:
        suggestions = SearchSuggestion.objects.filter(
            query__icontains=query, 
            is_active=True
        ).order_by('-weight')[:5]
        
        suggestion_list = [
            {'query': s.query, 'suggestion': s.suggestion} 
            for s in suggestions
        ]
        
        return JsonResponse({'suggestions': suggestion_list})
    
    return JsonResponse({'suggestions': []})
