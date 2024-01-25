from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreate, UserDetail, UserUpdate, UserDelete, UserList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreate.as_view(), name="register"),
    path("profiles/", UserList.as_view(), name="user_list"),
    path("profile/<pk>/", UserDetail.as_view(), name="user_retrieve"),
    path("profile/<pk>/update/", UserUpdate.as_view(), name="user_update"),
    path("profile/<pk>/delete/", UserDelete.as_view(), name="user_delete"),
]
