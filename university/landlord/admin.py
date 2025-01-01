# landlord/admin.py
from django.contrib import admin
from .models import Landlord

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_registered', 'is_verified', 'total_properties')
    list_filter = ('is_verified', 'date_registered')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address')
    date_hierarchy = 'date_registered'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'address')
        }),
        ('Business Information', {
            'fields': ('company_name', 'business_license', 'total_properties')
        }),
        ('Status', {
            'fields': ('is_verified',)
        })
    )