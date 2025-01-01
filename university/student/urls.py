# student/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='register'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('request-room/', views.request_room, name='request_room'),
    path('room-request/<int:request_id>/', views.view_room_request, name='view_room_request'),
    path('cancel-room-request/<int:request_id>/', views.cancel_room_request, name='cancel_room_request'),
]