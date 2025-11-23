from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import RestaurantReview, ReviewLike, MenuItemReview
from restaurants.models import Restaurant, MenuItem
from accounts.models import CustomUser


def restaurant_reviews(request, restaurant_id):
    """Display all reviews for a restaurant"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = RestaurantReview.objects.filter(restaurant=restaurant).select_related('user').prefetch_related('likes')
    
    context = {
        'restaurant': restaurant,
        'reviews': reviews,
    }
    return render(request, 'reviews/restaurant_reviews.html', context)


@login_required
def add_restaurant_review(request, restaurant_id):
    """Add a review for a restaurant"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        review_text = request.POST.get('review_text')
        
        # Check if user already reviewed this restaurant
        if RestaurantReview.objects.filter(user=request.user, restaurant=restaurant).exists():
            messages.error(request, 'You have already reviewed this restaurant.')
            return redirect('restaurants:restaurant_detail', restaurant_id=restaurant.id)
        
        # Create the review
        RestaurantReview.objects.create(
            user=request.user,
            restaurant=restaurant,
            rating=rating,
            title=title,
            review_text=review_text,
            is_verified_purchase=False  # Would need order verification logic
        )
        
        messages.success(request, 'Review added successfully!')
        return redirect('restaurants:restaurant_detail', restaurant_id=restaurant.id)
    
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'reviews/add_restaurant_review.html', context)


@login_required
def like_review(request, review_id):
    """Like a restaurant review"""
    if request.method == 'POST':
        review = get_object_or_404(RestaurantReview, id=review_id)
        
        # Check if user already liked this review
        like, created = ReviewLike.objects.get_or_create(
            user=request.user,
            review=review
        )
        
        if not created:
            # User already liked, so remove the like
            like.delete()
            review.likes_count = max(0, review.likes_count - 1)
            liked = False
        else:
            # New like
            review.likes_count += 1
            liked = True
        
        review.save(update_fields=['likes_count'])
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'liked': liked,
                'likes_count': review.likes_count
            })
        
        return redirect('reviews:restaurant_reviews', restaurant_id=review.restaurant.id)
    
    return redirect('restaurants:restaurant_list')
