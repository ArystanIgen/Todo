from rest_framework import serializers
from organization.models import Organization
from django.contrib.auth.models import Group, User
from auth_.serializers import UserSerializer
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin


class OrganizationSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = ['uuid', 'name', 'address', 'city', 'country', 'created_at', 'owner']

    def get_permissions_map(self, created):
        current_user = self.owner
        founder = Group.objects.create(name=f"{self.data['name']}_founder")
        support = Group.objects.create(name=f"{self.data['name']}_support")
        viewer = Group.objects.create(name=f"{self.data['name']}_viewer")
        current_user.groups.add(founder)
        return {
            'view_organization': [founder, support, viewer],
            'change_organization': [founder],
            'delete_organization': [founder],
            'add_organization': [founder],
            'view_task': [founder, support, viewer],
            'change_task': [founder, support],
            'add_task': [founder, support],
            'delete_task': [founder, support]
        }


class OrganizationInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    group = serializers.CharField(max_length=200)
    organization_name = serializers.CharField(max_length=200)

    def validate(self, data):
        group = data.get('group')
        if group not in ['viewer', 'support']:
            raise serializers.ValidationError("Group Error")
        organization_name = data.get('organization_name')
        fetched_organization = Organization.objects.get_organization_by_name(name=organization_name)
        if fetched_organization is None:
            raise serializers.ValidationError("There is no such organization")
        email = data.get("email")
        fetched_user = User.objects.get(email=email)
        if fetched_user is None:
            raise serializers.ValidationError("User with this email does not exist")
        return data

    def save(self):
        email = self.validated_data['email']
        group = self.validated_data['group']
        organization_name = self.validated_data['organization_name']
        fetched_user = User.objects.get(email=email)
        fetched_group = Group.objects.get(name=f"{organization_name}_{group}")
        fetched_user.groups.add(fetched_group)
