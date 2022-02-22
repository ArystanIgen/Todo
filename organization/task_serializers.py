from rest_framework import serializers
from organization.models import Organization, Task
from django.contrib.auth.models import Group, User
from auth_.serializers import UserSerializer
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin
from organization.organization_serializers import OrganizationSerializer


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    organization_id = serializers.StringRelatedField(read_only=True)
    organization_name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['uuid', 'name', 'description', 'created_at', 'user_id', 'organization_id', 'expiry_date',
                  'organization_name']

    def create(self, validated_data):
        validated_data['user_id'] = self.user_id
        validated_data['organization_id'] = self.organization_id
        return Task.objects.create(**validated_data)

    # def get_permissions_map(self, created):
    #     founder = Group.objects.get(name=f"{self.organization_name}_founder")
    #     support = Group.objects.get(name=f"{self.organization_name}_support")
    #     viewer = Group.objects.get(name=f"{self.organization_name}_viewer")
    #     return {
    #         'view_task': [founder, support, viewer],
    #         'change_task': [founder, support],
    #         'add_task': [founder, support],
    #         'delete_task': [founder, support]
    #     }
