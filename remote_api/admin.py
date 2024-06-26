from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Team)
admin.site.register(models.TeamInvitation)
admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.Feedback)