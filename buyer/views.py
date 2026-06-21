from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorite
# Create your views here.

@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, 'buyer/dashboard.html')


@login_required(login_url='accounts:login')
def favorites(request):
    favorite_listings = Favorite.objects.filter(user=request.user).select_related('listing')
    print(favorite_listings[0].user.first_name)
    return render(request, 'buyer/favorites.html', {'listings': favorite_listings})

@login_required(login_url='accounts:login')
def messages(request):
    return render(request, 'buyer/messages.html')

@login_required(login_url='accounts:login')
def conversation_detail(request, conversation_id):
    pass

@login_required(login_url='accounts:login')
def compare(request):
    pass

@login_required(login_url='accounts:login')
def profile(request):
    pass