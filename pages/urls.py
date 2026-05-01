from django.urls import path
from pages.views import *

app_name = "pages"

urlpatterns = [
    path("about/", about, name="about"),
    path("conatct/", contact, name="contact"),
    path("help/", help, name="help"),
    path("blog/", blog, name="blog"),
]