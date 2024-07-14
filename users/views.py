from rest_framework import viewsets
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, Profile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(pk=user.pk)

class GetAllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user.id)
    