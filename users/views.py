from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

# Resistration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # Saving user data
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) #password hashing
            user.save()
            messages.success(request, "Account created successfully")
            login(request, user) #Automatically log in user after registration
            return redirect('home') #Redirect to homepage
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Login
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# Logout
def logout_user(request):
    logout(request)
    return redirect('login') #Redirect to login page