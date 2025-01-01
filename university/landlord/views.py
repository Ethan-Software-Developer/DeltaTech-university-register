# landlord/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LandlordRegistrationForm
from .models import Landlord
from student.models import RoomRequest
from django.utils import timezone

def landlord_register(request):
    # First, log out any existing user
    logout(request)
    
    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Landlord.objects.create(user=user)
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('landlord_dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    else:
        form = LandlordRegistrationForm()
    
    return render(request, 'landlord/register.html', {'form': form})

def landlord_login(request):
    # First, log out any existing user
    logout(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            try:
                # Try to authenticate with email as username
                user = authenticate(username=email, password=password)
                if user is not None:
                    # Check if user has a landlord profile
                    if hasattr(user, 'landlord'):
                        login(request, user)
                        messages.success(request, 'Successfully logged in!')
                        return redirect('landlord_dashboard')
                    else:
                        messages.error(request, 'This account does not have landlord privileges.')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please enter both email and password.')
            
    return render(request, 'landlord/login.html')

def landlord_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('landlord-login')

@login_required
def landlord_dashboard(request):
    # Check if the user has a landlord profile
    if not hasattr(request.user, 'landlord'):
        logout(request)
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    try:
        pending_requests = RoomRequest.objects.filter(status='pending').order_by('-submitted_at')
        processed_requests = RoomRequest.objects.exclude(status='pending').order_by('-reviewed_at')
        
        context = {
            'landlord': request.user.landlord,
            'pending_requests': pending_requests,
            'processed_requests': processed_requests,
        }
        return render(request, 'landlord/dashboard.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('landlord-login')

@login_required
def process_request(request, request_id):
    # Check if the user has a landlord profile
    if not hasattr(request.user, 'landlord'):
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    if request.method == 'POST':
        try:
            room_request = get_object_or_404(RoomRequest, id=request_id)
            action = request.POST.get('action')
            notes = request.POST.get('notes', '')
            
            if action in ['accept', 'decline']:
                room_request.status = 'accepted' if action == 'accept' else 'declined'
                room_request.reviewed_at = timezone.now()
                room_request.reviewed_by = request.user.landlord
                room_request.notes = notes
                room_request.save()
                
                messages.success(
                    request, 
                    f'Room request {room_request.status} successfully.'
                )
            else:
                messages.error(request, 'Invalid action specified.')
        except Exception as e:
            messages.error(request, str(e))
    
    return redirect('landlord_dashboard')