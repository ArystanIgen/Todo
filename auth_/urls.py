from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import RegistrationAPIView, ChangePasswordAPIView, UpdateProfileView, UserDetail

app_name = 'auth_'
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('registration/', RegistrationAPIView.as_view()),
    path('api-token-refresh/', refresh_jwt_token),
    path('profile/<int:pk>/change_password', ChangePasswordAPIView.as_view(), name='auth_change_password'),
    path('profile/<int:pk>/update_profile', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('profile/<int:pk>/', UserDetail.as_view()),
]
