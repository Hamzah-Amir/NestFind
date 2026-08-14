from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from buyer.models import Inquiry

# Create your views here.

@login_required(login_url='accounts:login')
def dashboard(request):
    listings = Listing.objects.filter(agent=request.user)
    top_listings = listings.order_by('-views_count')[:5]
    listings_count = len(listings)
    views_count = listings.aggregate(Sum("views_count"))['views_count__sum'] or 0
    inquiries = Inquiry.objects.filter(listing__agent=request.user)
    recent_inquiries = inquiries.select_related('listing', 'buyer')[:5]
    print("Recent", recent_inquiries)
    inquiries_count = inquiries.count()
    context = {
        "listings": listings,
        "listings_count": listings_count,
        "top_listings": top_listings,
        "views_count": views_count,
        "recent_inquiry": recent_inquiries,
        "inquiries_count": inquiries_count,
        }
    return render(request, 'seller/dashboard.html', context)