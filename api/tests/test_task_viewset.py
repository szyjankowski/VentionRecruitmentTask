from rest_framework.test import APIClient, APITestCase
from rest_framework import status
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

    def test_read_task_list(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_task_detail(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse("task-list"),
            {
                "title": "new_task",
                "description": "new_task_description",
                "category": self.category.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        updated_data = {
            "title": "updated_task",
            "description": "updated_description",
            "category": self.category.id,
        }
        response = self.client.put(self.task_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "updated_task")
        self.assertEqual(self.task.description, "updated_description")

    def test_patch_task(self):
        patch_data = {"title": "patched_task"}
        response = self.client.patch(self.task_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "patched_task")

    def test_delete_task(self):
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_unauthenticated_user_cant_create_task(self):
        self.client.logout()
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse("task-list"),
            {
                "title": "new_task",
                "description": "new_task_description",
                "category": self.category.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 1)

    def test_unauthenticated_user_cant_update_task(self):
        self.client.logout()
        updated_data = {
            "title": "updated_task",
            "description": "updated_description",
            "category": self.category.id,
        }
        response = self.client.put(self.task_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.user.delete()
        Task.objects.all().delete()
        Category.objects.all().delete()
