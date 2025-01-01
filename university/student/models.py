from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class UniversityRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='university_registrations')
    university_name = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    start_date = models.DateField()
    university_student_id = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    documents = models.FileField(upload_to='university_docs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        'landlord.Landlord', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_university_registrations'
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'University Registration'
        verbose_name_plural = 'University Registrations'

    def __str__(self):
        return f"{self.student.user.username} - {self.university_name} ({self.status})"


class RoomRequest(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('studio', 'Studio Apartment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='room_requests')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    move_in_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in months")
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    special_requirements = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        'landlord.Landlord', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_room_requests'
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Room Request'
        verbose_name_plural = 'Room Requests'

    def __str__(self):
        return f"{self.student.user.username} - {self.room_type} ({self.status})"
