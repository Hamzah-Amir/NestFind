from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def listings(request):
    if request.method == "GET":
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 0)
        location = request.GET.get('location', '')
        property_type = request.GET.get('property_type', '')
    return HttpResponse("<h1>This is listing page</h1>")