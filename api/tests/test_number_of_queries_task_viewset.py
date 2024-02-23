from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from api.models import Task, Category
from django.urls import reverse


class TaskViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.category = Category.objects.create(name="test_category")
        self.task = Task.objects.create(
            title="test_task",
            description="test_description",
            completed=False,
            category=self.category,
        )
        self.client.force_authenticate(user=self.user)
        self.task_url = reverse("task-detail", kwargs={"pk": self.task.pk})

    def test_task_list_queries(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("task-list"))

    def test_task_detail_queries(self):
        with self.assertNumQueries(1):
            self.client.get(self.task_url)

    def test_task_create_queries(self):
        with self.assertNumQueries(2):
            self.client.post(
                reverse("task-list"),
                {
                    "title": "new_task",
                    "description": "new_task_description",
                    "category": self.category.id,
                },
            )

    def test_task_update_queries(self):
        with self.assertNumQueries(3):
            self.client.put(
                self.task_url,
                {
                    "title": "updated_task",
                    "description": "updated_description",
                    "category": self.category.id,
                },
            )

    def test_task_delete_queries(self):
        with self.assertNumQueries(2):
            self.client.delete(self.task_url)
