from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favorites/', views.favorites, name='favorites'),
    path('messages/', views.messages, name='messages'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('compare/', views.compare, name='compare'),
    path('profile/', views.profile, name='profile'),
]
