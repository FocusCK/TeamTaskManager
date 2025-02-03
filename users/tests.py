from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):

    def test_user_registration(self):
        # Send POST request to registration URL with form data
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'newuser@example.com',
        })

        # Check if user is redirected after successful registration (redirects to task list)
        self.assertRedirects(response, reverse('task_list'))

        # Verify that user was actually created in database
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')


class UserLoginTest(TestCase):

    def setUp(self):
        # Set up user to test login
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_user_login(self):
        # Send POST request to login wiht user credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123',
        })

        # Check if login is successful (redirect to task list after login)
        self.assertRedirects(response, reverse('task_list'))

        # Verify that user is logged in by checking sesion
        self.assertTrue('_auth_user_id' in self.client.session)