from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from organization import organization_views
from rest_framework.routers import DefaultRouter

app_name = 'organization'
# router = DefaultRouter()
#
# router.register('', views.OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', views.OrganizationViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<str:organization_id>/', views.OrganizationDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    )),
    path('<str:organization_id>/invite', views.OrganizationInviteViewSet.as_view(
        {
            'post': 'invite',
        }
    )),
]
