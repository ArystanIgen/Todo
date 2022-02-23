import logging
from typing import Optional, List, Tuple, Any
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from organization.exceptions import OrganizationNotFoundError, ProjectNotFoundError, UserNotPartOfOrganizationError
from organization.models import Organization, Project
from organization.serializers.project import ProjectSerializer
from organization.permissions import TaskObjectPermissions
from rest_framework_guardian import filters
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.GenericViewSet):
    serializer_class: ModelSerializer = ProjectSerializer
    permission_classes: Tuple = (TaskObjectPermissions,)
    pagination_class = LimitOffsetPagination

    filter_backends: List[Any] = [filters.ObjectPermissionsFilter]

    def get_object(self) -> Organization:
        organization_id: str = self.kwargs['organization_id']
        obj: Optional[Organization] = Organization.objects.get_organization_by_uuid(uuid=organization_id)
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self) -> List[Project]:
        return Project.objects.get_projects_by_organization(organization=self.get_object())

    @action(methods=['GET'], detail=False)
    def list(self, request, organization_id: str = None) -> Response:
        serializer = ProjectSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def create(self, request, organization_id: str = None) -> Response:
        serializer: ProjectSerializer = ProjectSerializer(data=request.data)
        fetched_user: Optional[User] = User.objects.filter(
            username=request.data["username"]
        ).first()
        fetched_organization: Organization = self.get_object()

        if fetched_user is None or not fetched_user.has_perm('view_organization', fetched_organization):
            raise UserNotPartOfOrganizationError

        serializer.user_id = fetched_user.id
        serializer.organization_id = fetched_organization.uuid

        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Created Project : {serializer.data['name']},by: {request.user.username}"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.warning(
            f"Project object cannot created/updated, errors: {serializer.errors}"
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailViewSet(viewsets.GenericViewSet):
    serializer_class: ProjectSerializer = ProjectSerializer
    permission_classes: Tuple = (TaskObjectPermissions,)

    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self) -> Optional[Project]:
        organization_id: str = self.kwargs['organization_id']
        project_id: str = self.kwargs['project_id']
        obj: Optional[Organization] = Organization.objects.get_organization_by_uuid(uuid=organization_id)
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        fetched_project: Optional[Project] = Project.objects.get_project_by_uuid(uuid=project_id)
        if fetched_project is None:
            raise ProjectNotFoundError
        return fetched_project

    def get_queryset(self) -> List[Project]:
        return Project.objects.all()

    @action(methods=['GET'], detail=True)
    def retrieve(self, request, organization_id: str = None, project_id: str = None) -> Response:
        serializer: ModelSerializer = self.serializer_class(self.get_object())
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=True)
    def destroy(self, request, organization_id: str = None, project_id: str = None) -> Response:
        fetched_project: Project = self.get_object()
        fetched_project.delete()
        return Response(
            {'status_message': 'Project has been removed successfully.'},
            status=status.HTTP_200_OK
        )
