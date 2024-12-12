from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ProfileForm
from .models import Plan

# Landing Page View
def landing(request):
    return render(request, 'landing_page.html')  # Ensure you have a landing_page.html template

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Home Page
@login_required
def home(request):
    plans = Plan.objects.filter(user=request.user, archived=False)
    return render(request, 'home.html', {'plans': plans})

# Create Plan
@login_required
def create_plan(request):
    if request.method == 'POST':
        # Handle form submission for creating a plan
        ...
    return render(request, 'create_plan.html')

# Create Event
@login_required
def create_event(request, plan_id):
    plans = Plan.objects.all()
    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == 'POST':
        # Handle form submission for creating an event
        ...
    return render(request, 'create_event.html', {'plan.id': plan})

# Profile View
@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

# Edit Profile
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})