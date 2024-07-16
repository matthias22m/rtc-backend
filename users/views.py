from django.urls import reverse_lazy
from rest_framework import viewsets
from django.views import View
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, Profile
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import render


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
class UserActivationView(View):
    template_name = 'activation.html'
    success_url = reverse_lazy('login')  

    def get(self, request, *args, **kwargs):
        print(kwargs,'----')
        uid = kwargs.get('uid')
        token = kwargs.get('token')
        return render(request, 'users/activate.html', {'uid':uid,'token':token })
    