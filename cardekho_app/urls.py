from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # For TokenAuthentication (optional, if you're using DRF's token auth)
    path('login/', obtain_auth_token, name='token_login'),

    # Custom Register and Logout views
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
