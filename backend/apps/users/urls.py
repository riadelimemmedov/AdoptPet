from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserRegisterationAPIView,
)

# from .views import hello_world


app_name = "users"
urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("", UserAPIView.as_view(), name="user-info"),
]
