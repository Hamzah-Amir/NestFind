from django.urls import path
from listings.views import *

app_name = "listings"

urlpatterns = [
    path("all", listings, name="listing"),
    path("featured/", listings, name="slug"),
    path("<slug:slug>/", detail, name="detail"),
]