from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Student, RoomRequest
from django.utils.dateparse import parse_date
from .forms import CustomUserCreationForm

# Define fixed room budgets
ROOM_BUDGETS = {
    'single': 3100,
    'double': 2600,
    'studio': 3200
}

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def student_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")

    form = CustomUserCreationForm()
    return render(request, 'student/register.html', {'form': form})

def student_login(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user immediately if they are already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            student, created = Student.objects.get_or_create(user=user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'student/login.html')  # Render the login form

@login_required
def student_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    room_requests = RoomRequest.objects.filter(student=student).order_by('-submitted_at')
    context = {
        'student': student,
        'room_requests': room_requests,
        'room_budgets': ROOM_BUDGETS,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def request_room(request):
    if request.method == "POST":
        student = get_object_or_404(Student, user=request.user)
        room_type = request.POST.get('room_type')
        move_in_date = request.POST.get('move_in_date')
        duration = request.POST.get('duration')
        budget = request.POST.get('budget')
        special_requirements = request.POST.get('special_requirements', '')

        # Debugging output
        print(f"Room Type Selected: {room_type}")

        # Validate required fields
        if not all([room_type, move_in_date, duration, budget]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('dashboard')

        # Normalize room_type and validate it
        room_type = room_type.lower()
        if room_type not in ROOM_BUDGETS:
            messages.error(request, 'Invalid room type selected.')
            return redirect('dashboard')

        # Validate budget
        expected_budget = ROOM_BUDGETS[room_type]
        try:
            submitted_budget = float(budget)
            if round(submitted_budget) != round(expected_budget):
                messages.error(request, 'Invalid budget amount for the selected room type.')
                return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Invalid budget value.')
            return redirect('dashboard')

        # Save the room request
        try:
            RoomRequest.objects.create(
                student=student,
                room_type=room_type,
                move_in_date=parse_date(move_in_date),
                duration=int(duration),
                budget=submitted_budget,
                special_requirements=special_requirements,
                status='pending'
            )
            messages.success(request, 'Room request submitted successfully!')
        except Exception as e:
            messages.error(request, f'Error saving room request: {str(e)}')
    return redirect('dashboard')

@login_required
def view_room_request(request, request_id):
    room_request = get_object_or_404(RoomRequest, id=request_id, student__user=request.user)
    return render(request, 'student/view_room_request.html', {'room_request': room_request})

@login_required
def cancel_room_request(request, request_id):
    room_request = get_object_or_404(RoomRequest, id=request_id, student__user=request.user)
    if room_request.status == 'pending':
        room_request.delete()
        messages.success(request, 'Room request cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel a processed room request.')
    return redirect('dashboard')
