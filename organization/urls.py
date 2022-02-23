from django.urls import path

from organization.views.organization import (OrganizationDetailViewSet,
                                             OrganizationInviteViewSet,
                                             OrganizationViewSet)
from organization.views.project import ProjectDetailViewSet, ProjectViewSet

app_name = 'organization'

urlpatterns = [
    path('', OrganizationViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<str:organization_id>/', OrganizationDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    )),
    path('<str:organization_id>/invite', OrganizationInviteViewSet.as_view(
        {
            'post': 'invite',
        }
    )),
    path('<str:organization_id>/tasks', ProjectViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('<str:organization_id>/tasks/<str:project_id>', ProjectDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    )),
]
