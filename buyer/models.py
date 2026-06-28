from django.db import models

# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.email} - {self.listing.title}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("responded", "Responded"),
        ("closed", "Closed"),
    ]

    buyer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='inquiries')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.buyer.email} → {self.listing.title}"