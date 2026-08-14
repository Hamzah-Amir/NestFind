from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

# Create your views here.

User = get_user_model()

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
    if request.method == "POST":
        role = request.POST.get("role", "buyer")
        if role not in ("buyer", "seller"):
            role = "buyer"

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        city = request.POST.get("city", "").strip()

        data = {
            "role": role,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }

        def fail(message):
            return render(request, "accounts/register.html", {"error": message, "form": data})

        if not email or not password:
            return fail("Email and password are required.")
        if password != confirm_password:
            return fail("Passwords do not match.")
        if User.objects.filter(email=email).exists():
            return fail("An account with this email already exists.")

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            city=city,
        )

        if role == "buyer":
            user.preferred_cities = request.POST.get("preferred_cities", "").strip()
            looking_for = request.POST.get("looking_for", "")
            user.looking_for = looking_for if looking_for in ("buy", "rent", "both") else None
        else:  # seller
            user.company_name = request.POST.get("company_name", "").strip()
        user.save()

        login(request, user)
        return redirect("core:home")

    return render(request, "accounts/register.html")