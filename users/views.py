from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, TeamForm, TeamMembershipForm
from django.contrib.auth.decorators import login_required
from .models import Team, TeamMembership, Company
from tasks.models import Task
from django.http import HttpResponseForbidden

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

@login_required
def create_team(request, company_id):
    company = Company.objects.get(id=company_id)

    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save(commit=False)
                team.company = company
                team.manager = request.user
                team.save()

                # To automatcally assign manager to the team
                TeamMembership.objects.create(user=request.user, team=team, role= 'Manager')

                return redirect('team_list', company_id=company.id)
            else:
                return render(request, 'users/create_team.html', {'form': form, 'company': company})
        else:
            form = TeamForm()
        return render(request, 'users/create_team.html', {'form': form, 'company': company})
            
    else:
        return HttpResponseForbidden("You don't have permission to create a team")

@login_required
def assign_role(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.user == team.manager:
        if request.method == 'POST':
            form = TeamMembershipForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('team_list', company_id=team.company.id)
        else:
            form = TeamMembershipForm(initial={'team': team})
        return render(request, 'users/assign_role.html', {'form': form, 'team': team})
    else:
        return redirect('home')
    
def team_list(request, company_id):
    # Get company based on company_id
    company = Company.objects.get(id=company_id)
    # Get all temas that belong to the company
    teams = Team.objects.filter(company=company)
    # Render team list with company and its teams
    return render(request, 'users/team_list.html', {'company': company, 'teams':teams})

@login_required
def dashboard(request):
    # Display the users tasks
    tasks = Task.objects.filter(assigned_to=request.user)

    # For managers' additional tasks
    if request.user.groups.filter(name='Manager').exists():
        teams = Team.objects.filter(manager=request.user)
        team_tasks = Task.objects.filter(team__in=teams)

        return render(request, 'users/dashboard_manager.html', {
            'tasks': tasks,
            'team_tasks': team_tasks,
            'teams': teams,
        })
    
    # For team members' tasks
    return render(request, 'users/dashboard_member.html', {
        'tasks': tasks
    })