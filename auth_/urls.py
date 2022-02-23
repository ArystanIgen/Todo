from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import RegistrationAPIView

app_name = 'auth_'

urlpatterns = [
    path(
        'login/',
        obtain_jwt_token
    ),
    path(
        'registration/', RegistrationAPIView.as_view()
    ),
    path(
        'api-token-refresh/',
        refresh_jwt_token
    ),

]
