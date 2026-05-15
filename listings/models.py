from django.db import models
from django.db.models import SET_NULL
from django.utils.text import slugify
from accounts.models import CustomUser
import uuid

# Create your models here.

class Listing(models.Model):
    STATUS_CHOICES = [
    ("draft", "Draft"),
    ("pending", "Pending"),
    ("active", "Active"),
    ("sold", "Sold"),
    ("rented", "Rented"),
    ("archived", "Archived"),
    ("deactivated", "Deactivated"),
]

    LISTING_TYPE_CHOICES = [
    ("for_sale", "For Sale"),
    ("for_rent", "For Rent"),
]
    
    PROPERTY_TYPE_CHOICES = [
    ("house", "House"),
    ("apartment", "Apartment"),
    ("flat", "Flat"),
    ("villa", "Villa"),
    ("plot", "Plot"),
    ("commercial", "Commercial"),
]
    UNIT_CHOICES = [("sqft", "Square Feet"), ("marla", "Marla"), ("kanal", "Kanal"), ("sqyd", "Square Yard")]

    FURNISHING_CHOICES = [
        ("furnished", "Furnished"),
        ("semi_furnished", "Semi Furnished"),
        ("unfurnished", "Unfurnished"),
        ("not_applicable", "Not Applicable"),
    ]

    NOC_CHOICES = [
        ("available", "Available"),
        ("pending", "Pending"),
        ("not_applicable", "Not Applicable"),
    ]

    agent = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=SET_NULL,
        null=True,
        related_name='listings'
    )
    
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=200)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    status = models.CharField(max_length=20, null=False, choices=STATUS_CHOICES)

    # Property details
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_negotiable = models.BooleanField(default=False)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    area_unit = models.CharField(max_length=20, null=False, choices=UNIT_CHOICES)
    bedrooms = models.PositiveIntegerField(null=True)
    bathrooms = models.PositiveIntegerField(null=True)
    floor_number = models.PositiveIntegerField(null=True)
    furnishing_status = models.CharField(max_length=50, null=True, choices=FURNISHING_CHOICES)
    noc_status = models.CharField(max_length=50, null=True, choices=NOC_CHOICES)

    # Location details
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    address = models.TextField()

    # Description
    description = models.TextField()

    # Featured 
    is_featured = models.BooleanField(default=False)
    featured_since = models.DateTimeField(null=True, blank=True)
    featured_until = models.DateTimeField(null=True, blank=True)

    # Tracking
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold_at = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        # Auto generate slug from title
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            slug = unique_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{unique_slug}-{counter}"
                counter += 1
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.listing.title}"