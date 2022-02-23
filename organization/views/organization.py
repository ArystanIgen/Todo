import logging
from typing import Optional, List
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from organization.exceptions import OrganizationExistsError, OrganizationNotFoundError
from organization.models import Organization
from organization.serializers.organization import OrganizationSerializer, OrganizationInviteSerializer
from organization.permissions import OrganizationObjectPermissions
from rest_framework_guardian import filters

logger = logging.getLogger(__name__)


class OrganizationViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> List[Organization]:
        return Organization.objects.all()

    @action(methods=['GET'], detail=False)
    def list(self, request) -> Response:
        serializer: OrganizationSerializer = OrganizationSerializer(
            self.get_queryset(), many=True
        )
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def create(self, request) -> Response:
        fetched_organization: Optional[Organization] = Organization.objects.get_organization_by_name(
            name=request.data['name']
        )
        if fetched_organization:
            raise OrganizationExistsError
        serializer: OrganizationSerializer = OrganizationSerializer(data=request.data)
        serializer.owner = request.user
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Created Organization : {serializer.data['name']},by: {request.user.username}"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(
            f"Organization object cannot created/updated, errors: {serializer.errors}"
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (OrganizationObjectPermissions,)
    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self) -> Optional[Organization]:
        organization_id: str = self.kwargs['organization_id']
        obj: Optional[Organization] = Organization.objects.get_organization_by_uuid(
            uuid=organization_id
        )
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        return obj

    @action(methods=['GET'], detail=True)
    def retrieve(self, request, organization_id: str) -> Response:
        fetched_organization: Optional[Organization] = Organization.objects.get_organization_by_uuid(
            uuid=organization_id
        )
        if fetched_organization is None:
            raise OrganizationNotFoundError
        serializer = self.serializer_class(fetched_organization)
        logger.info(
            f"Retrieved Organization: {serializer.data['name']}, by : {request.user.username}"
        )
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=True)
    def destroy(self, request, organization_id: str = None):
        fetched_organization: Optional[Organization] = self.get_object()
        fetched_organization.delete()
        logger.info(
            f"Deleted Organization : {fetched_organization.name}, by : {request.user.username}"
        )
        return Response(
            {'status_message': 'Organization has been removed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class OrganizationInviteViewSet(viewsets.GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationInviteSerializer
    permission_classes = (OrganizationObjectPermissions,)
    filter_backends = [filters.ObjectPermissionsFilter]

    def get_object(self) -> Organization:
        organization_id = self.kwargs['organization_id']
        obj = Organization.objects.get_organization_by_uuid(uuid=organization_id)
        if obj is None:
            raise OrganizationNotFoundError
        self.check_object_permissions(self.request, obj)
        return obj

    @action(methods=['POST'], detail=False)
    def invite(self, request, organization_id: str):
        fetched_organization: Organization = self.get_object()
        request.data["organization_name"] = fetched_organization.name
        serializer: OrganizationInviteSerializer = OrganizationInviteSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Invited User : {request.data['email']}"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
