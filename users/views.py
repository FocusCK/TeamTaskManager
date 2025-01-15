from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from tasks.models import Task

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
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('task_list')  # Redirect to task list after successful login
            else:
                messages.error(request, "Invalid login credentials")
    else:
        form = UserLoginForm()
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
