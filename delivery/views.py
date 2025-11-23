from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Delivery, DeliveryPerson
from orders.models import Order


def delivery_tracking(request, order_id):
    """Track delivery status for an order"""
    order = get_object_or_404(Order, id=order_id)
    
    try:
        delivery = Delivery.objects.get(order=order)
    except Delivery.DoesNotExist:
        delivery = None
    
    context = {
        'order': order,
        'delivery': delivery,
    }
    return render(request, 'delivery/tracking.html', context)


@login_required
def delivery_dashboard(request):
    """Dashboard for delivery personnel"""
    try:
        delivery_person = DeliveryPerson.objects.get(user=request.user)
        deliveries = Delivery.objects.filter(delivery_person=delivery_person).select_related('order', 'order__user')
    except DeliveryPerson.DoesNotExist:
        delivery_person = None
        deliveries = []
    
    context = {
        'delivery_person': delivery_person,
        'deliveries': deliveries,
    }
    return render(request, 'delivery/dashboard.html', context)


@login_required
def update_delivery_status(request, delivery_id):
    """Update delivery status"""
    from django.http import JsonResponse
    from django.utils import timezone
    
    if request.method == 'POST' and request.user.is_authenticated:
        delivery = get_object_or_404(Delivery, id=delivery_id)
        
        # Check if user is the assigned delivery person
        try:
            delivery_person = DeliveryPerson.objects.get(user=request.user)
            if delivery.delivery_person != delivery_person:
                return JsonResponse({'success': False, 'error': 'Not authorized'})
        except DeliveryPerson.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not a delivery person'})
        
        status = request.POST.get('status')
        if status in ['picked_up', 'in_transit', 'delivered']:
            delivery.status = status
            
            if status == 'delivered':
                delivery.delivered_time = timezone.now()
                delivery.actual_delivery_time = timezone.now()
            elif status == 'picked_up':
                delivery.pickup_time = timezone.now()
            elif status == 'in_transit':
                delivery.estimated_delivery_time = timezone.now()
            
            delivery.save()
            
            return JsonResponse({'success': True, 'status': status})
        
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
