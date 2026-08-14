from django.contrib import admin
from .models import Listing, ListingImage, ListingView

# Register your models here.
admin.site.register(Listing)
admin.site.register(ListingView)
admin.site.register(ListingImage)