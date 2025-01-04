from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

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
    return render(request, 'users/login.html', {'form': form})

# Logout
def logout_user(request):
    logout(request)
    return redirect('login') #Redirect to login page

@login_required
def home(request):
    return render(request, 'users/home.html')


# Must add the following to the tasks app(seperation of causes)
# def create_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('home')
#     else:
#         form = TaskForm()
#     return render(request, 'users/ceate_task.html', {'form': form})

# def update_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id, user=request.user)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'users/update_task.html', {'form': form})

# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id, user=request.user)
#     task.delete()
#     return redirect('home')