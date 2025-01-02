from django.contrib import admin
from django.urls import path, include
from university import views  # Correct import for views in the main project

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),  # Student app URLs
    path('landlord/', include('landlord.urls')),  # Landlord app URLs
    path('', views.index, name='index'),  # Example view from the main project views
]
