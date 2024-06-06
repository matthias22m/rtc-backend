from rest_framework import serializers
from .models import Project, Team, Task, Feedback
from django.contrib.auth import get_user_model


class UserSeializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=True
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserSeializer(
            instance.members.all(), many=True).data
        return representation


class ProjectSerializer(serializers.ModelSerializer):
    teams = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        many=True,
    )

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'created_date': {
                'read_only': True
            },
            'created_by': {
                'read_only': True
            }
        }


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=True,
        allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to', 'project']
        extra_kwargs = {'project': {
            'write_only': True
        }}


class FeedbackSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=False
    )

    class Meta:
        model = Feedback
        fields = '__all__'

        extra_kwargs = {
            'created_by': {
                'read_only': True
            }
        }
