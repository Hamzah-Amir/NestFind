from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ('agent', "Agent"),
        ("individual_seller", "Private Seller"),
        ("admin", "Admin"),
    ]


    objects = CustomUserManager()
    # Role
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')

    # Common fields for both roles
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    # Agent only fields
    agency_name = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_document = models.FileField(upload_to='license_documents/', blank=True, null=True)
    is_verified_agent = models.BooleanField(default=False)
    agency_logo = models.ImageField(upload_to='agency_logos/', blank=True, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    # Buyer only fields
    preferred_cities = models.CharField(max_length=255, blank=True, null=True)
    looking_for = models.CharField(
        max_length=10,
        choices=[("buy", "Buy"), ("rent", "Rent"), ("both", "Both")],
        null=True, blank=True
    )

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_agent(self):
        return self.role == 'agent'
    
    def is_buyer(self):
        return self.role == 'buyer'
    
    def is_individual_seller(self):
        return self.role == 'individual_seller'
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"