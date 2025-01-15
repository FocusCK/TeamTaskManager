from django.db import models
from django.contrib.auth.models import User

# Remove comment if I want to add custom user data in future eg. bio, profile pic
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username