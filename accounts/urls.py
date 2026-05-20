from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("users/login/", login_view, name="login"),
    path("users/register/", register_view, name="register"),
]
