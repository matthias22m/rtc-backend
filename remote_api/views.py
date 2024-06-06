from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import TeamSerializer, ProjectSerializer,TaskSerializer, FeedbackSerializer, UserSeializer
from .models import Team, Project, Task, Feedback
from .permissions import IsAuthorOrReadOnly


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('id')
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(teams__members=user) | Q(created_by=user)).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
        
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,IsAuthorOrReadOnly,)
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)

class TeamsInProjectViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id is not None:
            try:
                project = get_object_or_404(Project, pk=project_id)
                teams = project.teams.all()
                
                members = set()
                for team in teams:
                    members.update(team.members.all())
                return members
            except Project.DoesNotExist:
                return []
        else:
            return Team.objects.none()
    serializer_class = UserSeializer