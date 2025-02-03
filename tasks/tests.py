from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

class TaskModelTest(TestCase):

    def setUp(self):
        # Set up user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_task(self):
        # Log the user in
        self.client.login(username='testuser', password='testpassword')

        # Create task using form
        response = self.client.post(reverse('create_task'), {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': '2025-02-01T12:00:00Z',
            'completed': False
        })

        # Check task was created (check if redirects)
        self.assertRedirects(response, reverse('task_list'))

        # Check task exists in database
        task = Task.objects.get(title='Test Task')
        self.assertEqual(task.description, 'This is a test task.')
        self.assertEqual(task.user, self.user)
