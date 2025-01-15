# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.urls import reverse


# # Create your tests here.
# class TeamManagemenetTest(TestCase):

#     def setUp(self):
#         # Create dummy company
#         self.company = Company.objects.create(name="Test Company")
#         # Create dummy manager
#         self.manager = User.objects.create_user(username='manager', password='password')
#         # Assign manager the team manager
#         self.team_url = reverse('create_team', args=[self.company.id])
    
#     def test_manager_can_create_team(self):
#         """Test if a manager  can create a team in the company"""
#         self.client.login(username='manager', password='password')
#         # Request to make a team using POST
#         response = self.client.post(self.team_url, {'name': 'Product Development Team'})
#         # Chaeck team creation successful
#         self.assertEqual(response.status_code, 302) # Redirect if successful creation
#         self.assertRedirects(response, reverse('team_list', args=[self.company.id]))  # Check if redirected to team list

#         self.assertEqual(Team.objects.count(), 1) # Check team's been created
#         self.assertEqual(Team.objects.first().name, 'Product Development Team') # Check the name

#         self.assertEqual(Team.objects.first().manager, self.manager) #Check if manager is assigned

