from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from listings.models import Listing, ListingImage
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

@login_required(login_url='accounts:login')
def create_listings(request):
    if request.method == "POST":
        title = request.POST.get("title", '')
        price = request.POST.get("price", '')
        listing_type = request.POST.get("listing_type", '')
        property_type = request.POST.get("property_type", '')
        is_negotiable = 'price_negotiable' in request.POST
        city = request.POST.get('city', '')
        area = request.POST.get("area", '')
        address = request.POST.get('address', '')
        bedrooms = request.POST.get('bedrooms', '')
        bathrooms = request.POST.get('bathrooms', '')
        area_size = request.POST.get('area_size', '')
        area_unit = request.POST.get('area_unit', '')
        floor_number = request.POST.get('floor_number', '')
        furnishing_status = request.POST.get('furnishing_status', '')
        noc_status = request.POST.get('noc_status')
        description = request.POST.get('description')
        images = request.FILES.getlist('images', '')
        is_featured = 'is_featured' in request.POST
        status= request.POST.get('status', '')
        listing = Listing.objects.create(
            agent=request.user,
            title=title,
            price=price,
            listing_type=listing_type,
            property_type=property_type,
            price_negotiable=is_negotiable,
            city=city,
            area=area,
            address=address,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_size=area_size,
            area_unit=area_unit,
            floor_number=floor_number,
            furnishing_status=furnishing_status,
            noc_status=noc_status,
            description=description,
            is_featured=is_featured,
            status=status,
            )
        for image in images:
            ListingImage.objects.create(listing=listing, image=image)
            
        return redirect("seller:dashboard")
    return render(request, 'listings/create_listing.html')