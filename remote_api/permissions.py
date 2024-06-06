from rest_framework import permissions
from .models import Project

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            teams = obj.teams.all()
            members = set()
            for team in teams:
                members.update(team.members.all())
            if request.user in members:
                return True
            else:
                return False