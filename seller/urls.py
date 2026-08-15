from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/listing/add/', views.create_listings, name='create_listing'),
]
