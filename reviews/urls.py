from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('restaurant/<int:restaurant_id>/', views.restaurant_reviews, name='restaurant_reviews'),
    path('restaurant/<int:restaurant_id>/add/', views.add_restaurant_review, name='add_restaurant_review'),
    path('like/<int:review_id>/', views.like_review, name='like_review'),
]