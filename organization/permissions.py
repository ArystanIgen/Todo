from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class CustomObjectPermissions(permissions.DjangoObjectPermissions):

    def has_object_permission(self, request, view, obj):
        print("Objectdmfsdf")
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
            return request.user.has_perm('read_task', obj)
        if request.method in ['POST']:
            return request.user.has_perm('create_task', obj)
        if request.method in ['DELETE']:
            return request.user.has_perm('create_task', obj)
        return False
