from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"Category | {self.name}"


class Task(models.Model):
    title = models.TextField()
    description = models.TextField()
    completed = models.BooleanField()
    category = models.ForeignKey(
        Category, related_name="tasks", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Task | {self.title}"
