from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
import requests
from django.core.cache import cache


# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    sort_by = request.GET.get('sort_by', 'due_date')  # sort by 'due_date'
    if sort_by not in ['due_date', 'created_at']:
        sort_by = 'due_date'
    tasks = tasks.order_by(sort_by)
    quote = get_daily_quote()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'quote': quote, 'sort_by': sort_by})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

def get_daily_quote():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['slip']['advice']
    else:
        return "Failed to fetch quote."

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    sort_by = request.GET.get('sort_by', 'due_date')
    completion_status = request.GET.get('completion_status')
    quote = cache.get('quote_of_the_day')

    if not quote:
        # Get a new quote only if it's not cached
        quote = get_daily_quote()
        cache.set('quote_of_the_day', quote, timeout=86400)  # Cache for 24 hours
    if sort_by not in ['due_date', 'created_at']:
        sort_by = 'due_date'
    tasks = tasks.order_by(sort_by)
    if completion_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif completion_status == 'incomplete':
        tasks = tasks.filter(completed=False)

    return render(request, 'tasks/dashboard.html', {'tasks': tasks, 'quote': quote, 'sort_by': sort_by, 'completion_status': completion_status})
