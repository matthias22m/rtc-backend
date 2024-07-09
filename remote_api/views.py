from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .serializers import TeamSerializer, ProjectSerializer, TaskSerializer, FeedbackSerializer, UserSerializer, TeamInvitationSerializer
from .models import Team, Project, Task, Feedback, TeamInvitation
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import filters

UserModel = get_user_model()


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        user_instance = UserModel.objects.get(id=self.request.user.id)
        team.members.add(user_instance)
        team.save()


class TeamInvitationViewSet(viewsets.ModelViewSet):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return TeamInvitation.objects.filter(Q(user=user))


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('id')

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(teams__members=user) | Q(created_by=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','description']


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
    serializer_class = UserSerializer
