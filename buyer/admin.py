from django.contrib import admin
from .models import Favorite, Inquiry

# Register your models here.

admin.site.register(Favorite)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('listing__title', 'buyer__email', 'name', 'email')