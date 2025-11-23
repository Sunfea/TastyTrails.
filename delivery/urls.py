from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('track/<int:order_id>/', views.delivery_tracking, name='track_order'),
    path('dashboard/', views.delivery_dashboard, name='dashboard'),
    path('update/<int:delivery_id>/', views.update_delivery_status, name='update_status'),
]