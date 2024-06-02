from rest_framework import viewsets
from .serializers import TeamSerializer, ProjectSerializer,TaskSerializer, FeedbackSerializer
from .models import Team, Project, Task, Feedback
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    def get_queryset(self):
        user_id = self.request.user.id
        projects = Project.objects.filter(created_by = user_id)
        return projects
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
        
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)