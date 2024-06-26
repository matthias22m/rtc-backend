from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, ProjectViewSet, TaskViewSet, FeedbackViewSet, TeamsInProjectViewSet, TeamInvitationViewSet

router = DefaultRouter()

router.register(r'team',TeamViewSet, basename='team')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'task', TaskViewSet, basename='task')
router.register(r'feedback',FeedbackViewSet, basename='feedback')
router.register(r'team-invite',TeamInvitationViewSet, basename='teamInvite')
router.register(r'teams-in-project/(?P<project_id>\d+)', TeamsInProjectViewSet, basename='team-in-project')


urlpatterns = [
    path('', include(router.urls)),
]

