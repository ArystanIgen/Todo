from rest_framework import serializers

from organization.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True, read_only=True, max_length=200)
    user_id = serializers.IntegerField(read_only=True)
    organization_id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'uuid', 'name', 'description', 'created_at', 'user_id', 'organization_id', 'expiry_date', 'username'
        ]

    def create(self, validated_data):
        validated_data['user_id'] = self.user_id
        validated_data['organization_id'] = self.organization_id
        return Project.objects.create(**validated_data)
