from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Create your models here.

status_choices = [
    ('N', 'new'),
    ('O', 'ongoing'),
    ('T', 'terminated'),
    ('F', 'finished')
]


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(
        UserModel, blank=True, related_name='team-members+')
    def __str__(self) -> str:
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=status_choices, default='N')
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=status_choices)
    assigned_to = models.ManyToManyField(UserModel, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class Feedback(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.content 