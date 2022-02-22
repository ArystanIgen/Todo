from rest_framework import serializers
from organization.models import Organization, Task
from django.contrib.auth.models import Group, User
from auth_.serializers import UserSerializer
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin
from organization.organization_serializers import OrganizationSerializer


class TaskSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['uuid', 'name', 'address', 'city', 'country', 'created_at', 'user', 'organization']
