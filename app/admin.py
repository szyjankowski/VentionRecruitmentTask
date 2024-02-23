from django.contrib import admin
from app.models import Category, Task

# Register your models here.

admin.site.register(Category)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed", "category")
    list_filter = (
        "category",
        "completed",
    )
