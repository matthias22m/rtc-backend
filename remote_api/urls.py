from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import TeamViewSet, ProjectViewSet, TaskViewSet, FeedbackViewSet, TeamsInProjectViewSet, TeamInvitationViewSet

router = routers.DefaultRouter()

router.register(r'teams',TeamViewSet, basename='team')
router.register(r'projects', ProjectViewSet, basename='project')
# router.register(r'task', TaskViewSet, basename='task')
# router.register(r'feedbacks',FeedbackViewSet, basename='feedback')
router.register(r'team-invites',TeamInvitationViewSet, basename='teamInvite')
router.register(r'teams-in-projects/(?P<project_id>\d+)', TeamsInProjectViewSet, basename='team-in-project')
 

products_router = routers.NestedDefaultRouter(router,r'projects',lookup='project')
products_router.register('tasks',TaskViewSet, basename='project-tasks')
products_router.register('feedbacks',FeedbackViewSet,basename='project-feedback')
urlpatterns = router.urls + products_router.urls

