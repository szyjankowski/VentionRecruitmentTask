from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from app.models import Category, Task
from django.urls import reverse


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="example_user", password="example_password"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="example_category")
        self.category_url = reverse("category-detail", kwargs={"pk": self.category.pk})

    def test_unauthenticated_user_can_read_category_list(self):
        self.client.logout()
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_can_read_category_detail(self):
        self.client.logout()
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_category(self):
        self.assertEqual(Category.objects.count(), 1)
        response = self.client.post(reverse("category-list"), {"name": "new_category"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_authenticated_user_can_update_category(self):
        updated_data = {"name": "new_updated_category"}
        response = self.client.put(self.category_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "new_updated_category")

    def test_authenticated_user_can_delete_category(self):
        response = self.client.delete(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_authenticated_user_can_patch_category(self):
        updated_data = {"name": "patched_category"}
        response = self.client.patch(self.category_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "patched_category")

    def test_unauthenticated_user_cant_use_create_method(self):
        self.client.logout()
        self.assertEqual(Category.objects.count(), 1)
        response = self.client.post("/api/categories/", {"name": "new_category"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)

    def test_unauthenticated_user_cant_use_delete_method(self):
        self.client.logout()
        response = self.client.delete(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        self.user.delete()
        Category.objects.all().delete()
