from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from django.contrib import messages
from .models import Listing, ListingView
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
        return redirect('listings:detail', slug=listing.slug)

    if request.user != listing.agent:
        if request.user.is_authenticated:
            identify = {"user": request.user}
        else:
            if not request.session.session_key:
                request.session.create()          # anonymous users need a key first
        identity = {'session_key': request.session.session_key}

        already = ListingView.objects.filter(
        listing=listing,
        viewed_at__gte=timezone.now() - timedelta(hours=24),
        **identity,
    ).exists()

        if not already:
            ListingView.objects.create(listing=listing, **identity)
            Listing.objects.filter(pk=listing.pk).update(views_count=F('views_count') + 1)
        

    return render(request, "listings/detail.html", {'listing': listing})