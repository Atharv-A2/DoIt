from django.test import TestCase
from todo_app.models import Todo
from django.contrib.auth.models import User


class TodoModelTest(TestCase):
    def test_create_todo(self):
        """Test if the Todo is created correctly"""

        user = User.objects.create_user(username="testuser", password="testpassword")
        todo = Todo.objects.create(
            title="Write unit tests",
            description="Ensure full test coverage",
            status="WORKING",
            user=user,
        )
        self.assertEqual(todo.title, "Write unit tests")
        self.assertEqual(todo.status, "WORKING")
        self.assertIsNotNone(todo.timestamp)

    def test_default_status(self):
        """Test if the default status is OPEN"""
        user = User.objects.create_user(username="testuser", password="testpassword")
        todo = Todo.objects.create(
            title="Default Status Check",
            description="Status should be OPEN if not set",
            user=user,
        )
        self.assertEqual(todo.status, "OPEN")
