from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Listing
from buyer.models import Inquiry

# Create your views here.

def listings(request):
    if request.method == "GET":
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 0)
        location = request.GET.get('location', '')
        property_type = request.GET.get('property_type', '')
        filter = {}
        if min_price:
            filter['price__gte'] = min_price
        if max_price:
            filter['price__lte'] = max_price
        if location:
            filter['area'] = location
        if property_type:
            filter['property_type'] = property_type
        # Filtering listings based on the provided criteria
        listings = Listing.objects.filter(**filter)
        return render(request, "listings/listing.html", {'listings': listings})

def detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        Inquiry.objects.create(
            buyer=request.user,
            listing=listing,
            name=request.POST.get('name', '').strip() or request.user.get_full_name() or request.user.email,
            email=request.POST.get('email', '').strip() or request.user.email,
            phone=request.POST.get('phone', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, "Your inquiry has been sent to the agent.")
        return redirect('buyer:messages')

    return render(request, "listings/detail.html", {'listing': listing})