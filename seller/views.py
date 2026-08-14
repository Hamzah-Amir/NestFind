from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from listings.models import Listing

# Create your views here.

@login_required(login_url='accounts:login')
def dashboard(request):
    listings = Listing.objects.filter(agent=request.user)
    listings_count = len(listings)
    views_count = listings.aggregate(Sum("views_count"))
    print(views_count)
    context = {'listings': listings,"listings_count": listings_count}
    return render(request, 'seller/dashboard.html', context)