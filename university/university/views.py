# university/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'home.html')  # This will now use the home.html from the global templates folder
