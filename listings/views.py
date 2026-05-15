from django.http import HttpResponse
from django.shortcuts import render
from .models import Listing

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