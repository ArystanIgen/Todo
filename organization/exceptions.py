from rest_framework.exceptions import APIException


class OrganizationExistsError(APIException):
    status_code = 409
    default_detail = 'Organization with the same name already exists'
    default_code = 'OrganizationExists'


class OrganizationNotFoundError(APIException):
    status_code = 404
    default_detail = 'Organization not found'
    default_code = 'OrganizationNotFound'
