from typing import Dict, List, Optional

from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_guardian.serializers import \
    ObjectPermissionsAssignmentMixin

from auth_.serializers import UserSerializer
from organization.exceptions import GroupNotFoundError, UserNotFoundError
from organization.models import Organization


class OrganizationSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'address', 'city', 'country', 'created_at', 'owner']

    def get_permissions_map(self, created) -> Dict[str, List]:
        current_user = self.owner

        founder = Group.objects.create(name=f"{self.data['name']}_founder")
        support = Group.objects.create(name=f"{self.data['name']}_support")
        viewer = Group.objects.create(name=f"{self.data['name']}_viewer")

        current_user.groups.add(founder)

        fetched_permissions_project = Permission.objects.filter(
            codename__endswith="project"
        )
        fetched_permissions_organization_and_project = Permission.objects.filter(
            Q(codename__endswith="organization") | Q(codename__endswith="project")
        )
        view_permission = Permission.objects.filter(
            codename='view_project'
        ).first()

        founder.permissions.set(fetched_permissions_organization_and_project)
        support.permissions.set(fetched_permissions_project)

        viewer.permissions.add(view_permission)

        return {
            'view_organization': [founder, support, viewer],
            'change_organization': [founder],
            'delete_organization': [founder],
            'add_organization': [founder, support],
            'create_project': [founder, support],
            'read_project': [founder, support, viewer],
        }


class OrganizationInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    group = serializers.CharField(max_length=200)
    organization_name = serializers.CharField(allow_blank=True, max_length=200)

    def validate(self, data):
        group: str = data.get('group')
        if group not in ['viewer', 'support']:
            raise serializers.ValidationError("Group Error")
        return data

    def save(self):
        email: str = self.validated_data['email']
        group: str = self.validated_data['group']
        organization_name: str = self.validated_data['organization_name']

        fetched_user: Optional[User] = User.objects.get(email=email)
        if fetched_user is None:
            raise UserNotFoundError

        fetched_group: Optional[Group] = Group.objects.get(
            name=f"{organization_name}_{group}"
        )
        if fetched_group is None:
            raise GroupNotFoundError

        fetched_user.groups.add(fetched_group)
