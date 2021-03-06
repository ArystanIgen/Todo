import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


class OrganizationObjectPermissions(permissions.DjangoObjectPermissions):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return request.user.has_perm('view_organization', obj)
        if request.method in ['POST']:
            return request.user.has_perm('add_organization', obj)
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_perm('change_organization', obj)
        if request.method in ['DELETE']:
            return request.user.has_perm('delete_organization', obj)
        return False


class TaskObjectPermissions(permissions.DjangoObjectPermissions):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return request.user.has_perm('read_project', obj)
        if request.method in ['POST']:
            return request.user.has_perm('create_project', obj)
        if request.method in ['DELETE']:
            return request.user.has_perm('create_project', obj)
        return False
