from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class Todo(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE)

    status_choices = [
        ("OPEN", "Open"),
        ("WORKING", "Working"),
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("OVERDUE", "Overdue"),
        ("CANCELLED", "Cancelled"),
    ]
    status = models.CharField(max_length=20, default="OPEN", choices=status_choices)

    tags = models.TextField(blank=True)

    def set_tags(self, tag_list):

        # Convert list of tags to a comma-separated string
        unique_tags = list(set(tag_list))
        self.tags = ",".join(unique_tags)

    def get_tags(self):

        # Convert comma-separated string of tags to a list
        return self.tags.split(",") if self.tags else []

    def save(self, *args, **kwargs):
        # Ensure timestamp is set to current timezone-aware datetime if it is None
        if self.timestamp is None:
            self.timestamp = timezone.now()

        # Custom validation to ensure due_date is in the future if provided
        if self.due_date and self.due_date < self.timestamp:
            raise ValidationError("Due date cannot be before the creation timestamp.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
