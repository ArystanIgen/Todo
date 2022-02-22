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
from organization.models import Organization
from organization.organization_serializers import OrganizationSerializer, OrganizationInviteSerializer
from organization.permissions import CustomObjectPermissions
from rest_framework_guardian import filters

# from main.permissions import PublisherPermission, AuthorPermission

logger = logging.getLogger(__name__)


class OrganizationViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def list(self, request):
        serializer = OrganizationSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def create(self, request):
        fetched_organization: Organization = Organization.objects.get_organization_by_name(
            name=request.data['name']
        )
        if fetched_organization:
            raise OrganizationExistsError
        serializer = OrganizationSerializer(data=request.data)
        serializer.owner = request.user
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Score object cannot created/updated, errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (CustomObjectPermissions,)

    filter_backends = [filters.ObjectPermissionsFilter]

    @action(methods=['GET'], detail=True)
    def retrieve(self, request, organization_id: str = None):
        fetched_organization: Organization = Organization.objects.get_organization_by_uuid(
            uuid=organization_id
        )
        if fetched_organization is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(request, fetched_organization)

        serializer = self.serializer_class(fetched_organization)
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=True)
    def destroy(self, request, organization_id: str = None):
        fetched_organization: Organization = Organization.objects.get_organization_by_uuid(
            uuid=organization_id
        )
        if fetched_organization is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(request, fetched_organization)
        fetched_organization.delete()
        return Response(
            {'status_message': 'Organization has been removed successfully.'},
            status=status.HTTP_200_OK
        )


class OrganizationInviteViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationInviteSerializer
    permission_classes = (CustomObjectPermissions,)

    filter_backends = [filters.ObjectPermissionsFilter]

    @action(methods=['POST'], detail=True)
    def invite(self, request, organization_id: str):
        fetched_organization: Organization = Organization.objects.get_organization_by_uuid(
            uuid=organization_id
        )
        if fetched_organization is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(request, fetched_organization)
        serializer = OrganizationInviteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
