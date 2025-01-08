from django.db import models
from django.contrib.auth.models import User
from users.models import Team

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title