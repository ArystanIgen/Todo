import logging
from django.db.models import Avg, Max, Min, Sum, Count
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from organization.exceptions import OrganizationExistsError, OrganizationNotFoundError
from organization.models import Organization, Task
from organization.task_serializers import TaskSerializer
from organization.permissions import CustomObjectPermissions, TaskObjectPermissions
from rest_framework_guardian import filters

# from main.permissions import PublisherPermission, AuthorPermission

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = (TaskObjectPermissions,)

    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self):
        organization_id = self.kwargs['organization_id']
        obj = Organization.objects.get_organization_by_uuid(uuid=organization_id)
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Task.objects.get_tasks_by_organization(organization=self.get_object())

    @action(methods=['GET'], detail=False)
    def list(self, organization_id: str = None):
        serializer = TaskSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def create(self, request, organization_id: str = None):
        serializer = TaskSerializer(data=request.data)
        serializer.user_id = request.user.id
        fetched_organization = self.get_object()
        serializer.organization_id = fetched_organization.uuid
        serializer.organization_name = fetched_organization.name
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Score object cannot created/updated, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailViewSet(viewsets.GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = (TaskObjectPermissions,)

    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self):
        organization_id = self.kwargs['organization_id']
        task_id = self.kwargs['task_id']
        obj = Organization.objects.get_organization_by_uuid(uuid=organization_id)
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        fetched_task = Task.objects.get_task_by_uuid(uuid=task_id)
        return fetched_task

    def get_queryset(self):
        return Task.objects.get_tasks_by_organization(organization=self.get_object())

    @action(methods=['GET'], detail=True)
    def retrieve(self, request, organization_id: str = None, task_id: str = None):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=True)
    def destroy(self, request, organization_id: str = None, task_id: str = None):
        fetched_task = self.get_object()
        fetched_task.delete()
        return Response(
            {'status_message': 'Organization has been removed successfully.'},
            status=status.HTTP_200_OK
        )
