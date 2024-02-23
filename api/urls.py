from api.views import CategoryViewSet, TaskViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [path("auth/", include("rest_framework.urls"))] + router.urls
