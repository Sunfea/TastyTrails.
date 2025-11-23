from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:order_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:order_item_id>/', views.update_cart_item, name='update_cart_item'),
]