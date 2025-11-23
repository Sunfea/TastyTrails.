from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Restaurant, Cuisine, RestaurantCuisine, MenuItem


def restaurant_list(request):
    try:
        # Optimize the base query with better prefetching
        restaurants = Restaurant.objects.filter(is_active=True).select_related('owner').prefetch_related(
            'hours', 
            'restaurantcuisine_set__cuisine',
            'menu_items'
        )
        
        # Filter by cuisine if provided
        cuisine_id = request.GET.get('cuisine')
        if cuisine_id:
            try:
                restaurants = restaurants.filter(restaurantcuisine__cuisine_id=cuisine_id).distinct()
            except ValueError:
                # Invalid cuisine_id, ignore filter
                pass
        
        # Search by name or menu items if provided
        search_query = request.GET.get('search')
        if search_query:
            # Search in restaurant names, descriptions, and menu item names/descriptions
            restaurants = restaurants.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(menu_items__name__icontains=search_query) |
                Q(menu_items__description__icontains=search_query)
            ).distinct()
        
        # Order by rating (already in meta, but explicit ordering for clarity)
        restaurants = restaurants.order_by('-rating')
        
        # Pagination
        paginator = Paginator(restaurants, 10)  # Show 10 restaurants per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all cuisines for filter dropdown (cache this in production)
        cuisines = Cuisine.objects.all()
        
        context = {
            'page_obj': page_obj,
            'cuisines': cuisines,
            'selected_cuisine': int(cuisine_id) if cuisine_id and cuisine_id.isdigit() else None,
            'search_query': search_query,
        }
        return render(request, 'restaurants/restaurant_list.html', context)
    except Exception as e:
        # Log the error in production
        context = {
            'page_obj': [],
            'cuisines': [],
            'selected_cuisine': None,
            'search_query': '',
            'error': 'An error occurred while fetching restaurants. Please try again later.'
        }
        return render(request, 'restaurants/restaurant_list.html', context)


def restaurant_detail(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.select_related('owner').prefetch_related(
            'hours', 'menu_items', 'reviews'
        ).get(id=restaurant_id)
        
        # Group menu items by category if needed in the future
        menu_items = restaurant.menu_items.filter(is_available=True)
        
        context = {
            'restaurant': restaurant,
            'menu_items': menu_items,
        }
        return render(request, 'restaurants/restaurant_detail.html', context)
    except Restaurant.DoesNotExist:
        from django.http import Http404
        raise Http404("Restaurant not found")