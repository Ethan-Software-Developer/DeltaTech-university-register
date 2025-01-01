# landlord/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_registered = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    
    # Additional fields you might want:
    company_name = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.CharField(max_length=50, blank=True, null=True)
    total_properties = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'landlord_registration'
        verbose_name = 'Landlord'
        verbose_name_plural = 'Landlords'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone_number}"