from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        print(f"Attempting to authenticate user with email: {email}")
        if user is not None:
            login(request, user)
            print(f"User {email} authenticated successfully.")
            return redirect("core:home")
        else:
            print(f"Failed to authenticate user with email: {email}")
            return render(request, "accounts/login.html", {"error": "Invalid email or password."})
        
    return render(request, "accounts/login.html")

def register_view(request):
    return render(request, "accounts/register.html")