from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from organization import organization_views, task_views
from rest_framework.routers import DefaultRouter

app_name = 'organization'

urlpatterns = [
    path('', organization_views.OrganizationViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<str:organization_id>/', organization_views.OrganizationDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    )),
    path('<str:organization_id>/invite', organization_views.OrganizationInviteViewSet.as_view(
        {
            'post': 'invite',
        }
    )),
    path('<str:organization_id>/tasks', task_views.TaskViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('<str:organization_id>/tasks/<str:task_id>', task_views.TaskDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    )),
]
