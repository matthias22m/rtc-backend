from rest_framework import serializers
from .models import Project, Team, Task, Feedback, TeamInvitation
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'owner': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserSerializer(
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

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'updated_time',
                  'status', 'assigned_to']
        extra_kwargs = {'id': {'read_only': True},
                        'updated_time': {'read_only': True}}

    def create(self, validated_data):
        project_id = self.context['project_id']
        return Task.objects.create(project_id=project_id, **validated_data)


class TeamInvitationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        many=False
    )
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        many=False
    )

    class Meta:
        model = TeamInvitation
        fields = ['id', 'user', 'team', 'is_accepted']
        extra_kwargs = {'id': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(
            instance.user, many=False).data
        representation['team'] = TeamSerializer(
            instance.team, many=False).data
        return representation


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['content', 'created_date', 'created_by']

        extra_kwargs = {
            'created_by': {
                'read_only': True
            }, 'created_date': {
                'read_only': True
            }}

    def create(self, validated_data):
        project_id = self.context['project_id']
        return Feedback.objects.create(project_id=project_id, **validated_data)
    
    def to_representation(self, instance: Feedback):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by, many=False).data
        representation['project'] = ProjectSerializer(instance.project, many=False).data
        return representation