from rest_framework.exceptions import APIException


class OrganizationExistsError(APIException):
    status_code = 409
    default_detail = 'Organization with the same name already exists'
    default_code = 'OrganizationExists'


class OrganizationNotFoundError(APIException):
    status_code = 404
    default_detail = 'Organization not found'
    default_code = 'OrganizationNotFound'


class ProjectNotFoundError(APIException):
    status_code = 404
    default_detail = 'Project not found'
    default_code = 'ProjectNotFound'


class UserNotFoundError(APIException):
    status_code = 404
    default_detail = 'User not found'
    default_code = 'UserNotFound'


class GroupNotFoundError(APIException):
    status_code = 404
    default_detail = 'Group not found'
    default_code = 'GroupNotFound'


class UserNotPartOfOrganizationError(APIException):
    status_code = 404
    default_detail = 'User is not part of this organization'
    default_code = 'UserNotPartOfOrganization'
