from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .forms import LandlordRegistrationForm
from .models import Landlord
from student.models import RoomRequest

# Define the security key (in production, this should be in environment variables)
SECURITY_KEY = "LANDLORD2024"  # Change this to your desired security key

def landlord_register(request):
    # First, log out any existing user
    logout(request)
    
    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        security_key = request.POST.get('securityKey')
        
        # First check the security key
        if security_key != SECURITY_KEY:
            messages.error(request, 'Invalid security key.')
            return render(request, 'landlord/register.html', {'form': form})
        
        if form.is_valid():
            try:
                # Create user but don't save yet
                user = form.save(commit=False)
                
                # Set username equal to email
                user.username = user.email
                
                # Check if username/email already exists
                if User.objects.filter(username=user.username).exists():
                    messages.error(request, 'An account with this email already exists.')
                    return render(request, 'landlord/register.html', {'form': form})
                
                # If all is well, save the user
                user.save()
                
                # Create the landlord profile
                Landlord.objects.create(user=user)
                
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('landlord-login')
                
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
        pending_requests = RoomRequest.objects.filter(
            room__landlord=request.user.landlord,
            status='pending'
        ).order_by('-submitted_at')
        
        processed_requests = RoomRequest.objects.filter(
            room__landlord=request.user.landlord
        ).exclude(status='pending').order_by('-reviewed_at')
        
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
            room_request = get_object_or_404(
                RoomRequest,
                id=request_id,
                room__landlord=request.user.landlord
            )
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
                    f'Room request has been {room_request.status}.'
                )
            else:
                messages.error(request, 'Invalid action specified.')
        except RoomRequest.DoesNotExist:
            messages.error(request, 'Room request not found.')
        except Exception as e:
            messages.error(request, str(e))
    
    return redirect('landlord_dashboard')

@login_required
def profile_settings(request):
    # Check if the user has a landlord profile
    if not hasattr(request.user, 'landlord'):
        logout(request)
        messages.error(request, 'You do not have landlord privileges.')
        return redirect('landlord-login')
    
    if request.method == 'POST':
        try:
            # Update profile information
            landlord = request.user.landlord
            landlord.phone = request.POST.get('phone', '')
            landlord.address = request.POST.get('address', '')
            landlord.save()
            
            # Update user information
            user = request.user
            user.first_name = request.POST.get('name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Failed to update profile: {str(e)}')
            
    context = {
        'landlord': request.user.landlord
    }
    return render(request, 'landlord/profile_settings.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully. Please login again.')
            return redirect('landlord-login')
            
    return render(request, 'landlord/change_password.html')