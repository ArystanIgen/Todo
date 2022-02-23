import logging

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from auth_.models import Profile, User

logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=120,
        min_length=8,
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
