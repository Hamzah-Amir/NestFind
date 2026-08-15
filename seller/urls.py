from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listing/add/', views.create_listings, name='create_listing'),
    path('listings/', views.my_listings, name='listings'),
    path('listings/<slug:slug>/delete/', views.delete_listings, name='delete_listings'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('setting/', views.settings, name='settings'),
]
