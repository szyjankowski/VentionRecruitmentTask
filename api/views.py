from app.models import Category, Task
from api.serializers import TaskSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
