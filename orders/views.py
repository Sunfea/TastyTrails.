from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from restaurants.models import MenuItem
from .models import Order, OrderItem


@login_required
def add_to_cart(request, menu_item_id):
    """Add a menu item to the user's cart"""
    if request.method == 'POST':
        try:
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            quantity = int(request.POST.get('quantity', 1))
            
            # Validate quantity
            if quantity <= 0:
                messages.error(request, 'Quantity must be at least 1')
                return redirect('restaurants:restaurant_detail', restaurant_id=menu_item.restaurant.id)
            
            # Get or create an active order for the user
            order, created = Order.objects.get_or_create(
                user=request.user,
                restaurant=menu_item.restaurant,
                status='pending'
            )
            
            # Check if item already exists in cart
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                menu_item=menu_item,
                defaults={'quantity': quantity, 'price': menu_item.price}
            )
            
            if not created:
                order_item.quantity += quantity
                order_item.save()
            
            # Update order total
            order_items = order.items.all()
            total = sum(item.total_price for item in order_items)
            order.total_amount = total
            order.save(update_fields=['total_amount'])
            
            messages.success(request, f'{menu_item.name} added to cart!')
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'{menu_item.name} added to cart!',
                    'item_count': order.items.count()
                })
            
            return redirect('restaurants:restaurant_detail', restaurant_id=menu_item.restaurant.id)
        except Exception as e:
            messages.error(request, 'Error adding item to cart. Please try again.')
            return redirect('restaurants:restaurant_list')
    
    return redirect('restaurants:restaurant_list')

@login_required
def view_cart(request):
    """View the user's cart"""
    # Get the user's pending order
    try:
        order = Order.objects.get(user=request.user, status='pending')
        items = order.items.all()
        total = sum(item.total_price for item in items)
        # Update the order's total_amount
        order.total_amount = total
        order.save(update_fields=['total_amount'])
    except Order.DoesNotExist:
        order = None
        items = []
        total = 0
    
    return render(request, 'orders/cart.html', {
        'order': order,
        'items': items,
        'total': total
    })

@login_required
def remove_from_cart(request, order_item_id):
    """Remove an item from the cart"""
    if request.method == 'POST':
        try:
            order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
            order = order_item.order
            order_item.delete()
            
            # Update order total
            order_items = order.items.all()
            total = sum(item.total_price for item in order_items) if order_items.exists() else 0
            order.total_amount = total
            order.save(update_fields=['total_amount'])
            
            messages.success(request, 'Item removed from cart!')
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart!'
                })
            
            return redirect('orders:view_cart')
        except Exception as e:
            messages.error(request, 'Error removing item from cart. Please try again.')
            return redirect('orders:view_cart')
    
    return redirect('orders:view_cart')

@login_required
def update_cart_item(request, order_item_id):
    """Update quantity of an item in the cart"""
    if request.method == 'POST':
        try:
            order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
            quantity = int(request.POST.get('quantity', 1))
            
            # Validate quantity
            if quantity < 0:
                messages.error(request, 'Quantity cannot be negative')
                return redirect('orders:view_cart')
            
            if quantity == 0:
                order_item.delete()
            else:
                order_item.quantity = quantity
                order_item.save()
            
            # Update order total
            order = order_item.order
            order_items = order.items.all()
            total = sum(item.total_price for item in order_items)
            order.total_amount = total
            order.save(update_fields=['total_amount'])
            
            messages.success(request, 'Cart updated!')
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Cart updated!',
                    'new_quantity': quantity if quantity > 0 else 0
                })
            
            return redirect('orders:view_cart')
        except Exception as e:
            messages.error(request, 'Error updating cart. Please try again.')
            return redirect('orders:view_cart')
    
    return redirect('orders:view_cart')
