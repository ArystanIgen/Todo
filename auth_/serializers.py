from rest_framework import serializers
from auth_.models import User, Profile
from django.contrib.auth.password_validation import validate_password
import logging

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        required=True,
        validators=[validate_password],
        write_only=True
    )
    password2 = serializers.CharField(required=True, write_only=True)
    old_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password1": "Password fields didn't match."})
        return attrs

    def validate_old(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password1'])
        instance.save()

        logger.info(f"Paasword change, user: {user}")
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'role',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if Profile.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def validate_username(self, value):
        user = self.context['request'].user

    def update(self, instance, validated_data):

        user = self.context['request'].user

        if user.profile.pk != instance.pk:
            logger.error('Other person tried to enter!')
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.phone_number = validated_data['phone_number']
        instance.save()

        logger.info(f"Profile information change, user: {user}")
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
