from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from .serializers import RegistrationSerializer, ChangePasswordSerializer, UpdateUserSerializer, UserSerializer
from .models import User, Profile
import logging

logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(f"Registered new user, user: {user}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class UserDetail(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk, *args, **kwargs):
        profile = User.objects.get(pk=pk)
        if request.user.profile.pk != profile.pk:
            return Response(status=status.HTTP_423_LOCKED)

        return self.retrieve(request, *args, **kwargs)
