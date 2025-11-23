from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search, name='search'),
    path('suggestions/', views.search_suggestions, name='search_suggestions'),
]