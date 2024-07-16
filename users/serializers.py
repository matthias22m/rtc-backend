from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=False
    )

    class Meta:
        model = Profile
        fields = ['user', 'image']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'profile', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }
        ref_name = 'UserSerializer_users'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile'] = ProfileSerializer(
            instance.profile, many=False).data['image']
        return representation

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active=False
        instance.save()

        return instance
