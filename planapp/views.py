from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ProfileForm, PlanForm, EventForm
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
            messages.error(request, "Registration failed. Please correct the errors below.")
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
            messages.error(request, "Invalid credentials. Please try again.")
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
    form = PlanForm()

    if request.method == 'POST':
        form = PlanForm(request.POST)

        if form.is_valid():
            # Assign the current logged-in user to the plan before saving
            plan = form.save(commit=False)
            plan.user = request.user  # Set the user to the currently logged-in user
            plan.save()  # Save the plan to the database

            messages.success(request, 'Plan created successfully!')
            return redirect('home')  # Redirect to home after successful creation
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'create_plan.html', {'form': form})


# Create Event
@login_required
def create_event(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.plan = plan
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to create event. Please correct the errors below.")
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form, 'plan': plan})


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
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Failed to update profile. Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


def plan_detail(request, plan_id):
    # Get the plan using the plan_id
    plan = get_object_or_404(Plan, id=plan_id)

    # Render the template with the plan object
    return render(request, 'plan-detail.html', {'plan': plan})


def edit_plan(request):
    plan = get_object_or_404(Plan, id=id)

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan-detail', id=plan.id)
    else:
        form = PlanForm(instance=plan)

    return render(request, 'edit_plan.html', {'form': form, 'plan': plan})
def delete_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        return redirect('home')  # Redirect to home after deletion
    return render(request, 'delete-plan.html', {'plan': plan})