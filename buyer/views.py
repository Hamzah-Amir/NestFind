from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite, Inquiry
# Create your views here.

@login_required(login_url='accounts:login')
def dashboard(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    inquiries = Inquiry.objects.filter(buyer=request.user).select_related('listing')

    context = {
        'favorites_count': favorites.count(),
        'inquiries_count': inquiries.count(),
        'pending_count': inquiries.filter(status='pending').count(),
        'recent_favorites': favorites[:3],
        'recent_inquiries': inquiries[:3],
    }
    return render(request, 'buyer/dashboard.html', context)


@login_required(login_url='accounts:login')
def favorites(request):
    favorite_listings = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'buyer/favorites.html', {'favorites': favorite_listings})

@login_required(login_url='accounts:login')
def messages(request):
    inquiries = Inquiry.objects.filter(buyer=request.user).select_related('listing', 'listing__agent')
    return render(request, 'buyer/messages.html', {'inquiries': inquiries})

@login_required(login_url='accounts:login')
def conversation_detail(request, conversation_id):
    pass

@login_required(login_url='accounts:login')
def compare(request):
    pass

@login_required(login_url='accounts:login')
def profile(request):
    pass
