from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('task_list')  # Redirect to task list page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# User Login
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Redirect to task list after successful login
            else:
                messages.error(request, "Invalid login credentials")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

# User Logout
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logging out

# Home Page
@login_required
def home(request):
    return render(request, 'users/home.html')

# User Dashboard (Shows tasks for the logged-in user)
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {'tasks': tasks})

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #Keep uer logged in after password change
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('profile_settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/profile_settings.html', {'form': form})