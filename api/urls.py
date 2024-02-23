from api.views import CategoryViewSet, TaskViewSet, CreateUserView, logout_view
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("auth/logout/", logout_view, name="logout"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/register/", CreateUserView.as_view(), name="register"),
    path("auth/api-token-auth/", obtain_auth_token, name="api-token-auth"),
] + router.urls
