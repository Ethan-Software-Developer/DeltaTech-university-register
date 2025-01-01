# landlord/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.landlord_login, name='landlord-login'),
    path('register/', views.landlord_register, name='landlord-register'),
    path('logout/', views.landlord_logout, name='landlord_logout'),
    path('dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('process-request/<int:request_id>/', views.process_request, name='process_request'),  # Changed to match view function name
]