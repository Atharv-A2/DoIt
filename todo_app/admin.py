from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "due_date", "timestamp")
    list_filter = ("status", "due_date")
    search_support = ("title", "description")
    readonly_fields = ("timestamp",)

    fieldsets = (
        ("Basic Info", {"fields": ("title", "description", "status")}),
        ("Additional Details", {"fields": ("due_date", "tags")}),
        ("Timestamps", {"fields": ("timestamp",), "classes": ("collapse",)}),
    )


admin.site.register(Todo, TodoAdmin)
