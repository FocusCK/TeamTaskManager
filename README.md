# Team Task Manager

A web application to help individuals manage their tasks with features like creating, updating, and deleting tasks, as well as a dashboard for tracking progress. Users can register, log in, and view a list of tasks with options to sort and filter.

## Features

- **User Registration and Authentication**: Users can create accounts, log in, and log out.
- **Task Management**: Users can add, edit, and delete tasks. Tasks are displayed in a card format on the task list.
- **Sorting Tasks**: Users can sort tasks by due date or date created.
- **Responsive Layout**: The app is designed to be mobile-friendly with a collapsible navbar for small screens.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/team-task-manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd team-task-manager
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the app in your browser:

   ```
   http://127.0.0.1:8000/
   ```

## Code Snippets

### User Registration View

In `users/views.py`:

```python
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('task_list')  # Redirect to task list after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
```

### Task List View

In `tasks/views.py`:

```python
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
```

### Task Model

In `tasks/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

### Task List HTML Template

In `tasks/templates/tasks/task_list.html`:

```html
{% extends 'users/base.html' %}

{% block title %}Your Tasks{% endblock %}

{% block content %}
<h2>Your Tasks</h2>

<div class="task-container">
    {% for task in tasks %}
        <div class="card">
            <h5>{{ task.title }}</h5>
            <p>{{ task.description }}</p>
            <p><strong>Due:</strong> {{ task.due_date }}</p>
            <p><strong>Status:</strong> {% if task.completed %}Completed{% else %}Incomplete{% endif %}</p>
            <a href="{% url 'update_task' task.id %}">Edit</a>
            <a href="{% url 'delete_task' task.id %}">Delete</a>
        </div>
    {% endfor %}
</div>
{% endblock %}
```

## Future Developments

1. **Email Reminders**: Implement email notifications to remind users of upcoming tasks.
2. **Task Prioritization**: Add a priority field for tasks, allowing users to prioritize tasks (High, Medium, Low).
3. **Task Categories**: Allow users to categorize tasks by adding a category field (e.g., Work, Personal).
4. **API Integration**: Integrate an API (e.g., a weather API or quote API) to enhance user experience with daily inspirational quotes or weather forecasts.
5. **Task History**: Allow users to view a history of completed tasks, providing insights into their task management.
