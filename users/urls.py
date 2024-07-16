from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GetAllUserViewSet, ProfileViewSet, UserActivationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


router = DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'all-user', GetAllUserViewSet, basename='all-user')
router.register(r'profile', GetAllUserViewSet, basename='profile')

urlpatterns = [

    path('<str:uid>/<str:token>/', UserActivationView.as_view(), name='user-activation'),
    # path('', include(router.urls)),
    # path('all-user/', ProfileViewSet.as_view({'get': 'list'}), name='user-list'),
    # path('profile/<int:pk>/', ProfileViewSet.as_view({'get': 'retrive', 'put':'update', 'delete': 'destroy'}), name='profile-detail'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
