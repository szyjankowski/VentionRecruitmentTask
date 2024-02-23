from app.models import Category, Task
from api.serializers import TaskSerializer, CategorySerializer, UserSerializer
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if category_id := self.request.query_params.get("category"):
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


#  Since django 4.1.0 logout views has to be POST method for security reasons
#  https://forum.djangoproject.com/t/deprecation-of-get-method-for-logoutview/25533
@api_view(["POST"])
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return Response(status=status.HTTP_200_OK)
