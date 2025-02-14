from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from todo_app.models import Todo


class TodoAPITest(APITestCase):
    def setUp(self):
        """Create a sample To-Do before each test"""

        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.todo = Todo.objects.create(
            title="Integration Test",
            description="Testing API endpoints",
            status="OPEN",
            tags="Django, Testing, API",
            user=self.user,
        )

        self.todo_url = reverse("todo-detail", args=[self.todo.id])
        self.todo_list_url = reverse("todo-list-create")
        self.client = APIClient()

    def authenticate(self):
        """Manually Authenticate by logging in and getting the token"""
        self.client.force_authenticate(user=self.user)

    def test_create_todo(self):
        """Test Creating a new todo"""

        self.authenticate()  # Ensure the user is authenticated

        data = {
            "title": "New Task",
            "description": "Test API create",
            "status": "WORKING",
            "tags": "Django, Testing, API",
        }

        response = self.client.post(self.todo_list_url, data, format="json")
        # print(response.content)
        # print(response.status_code)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Task")

    def test_get_todos(self):
        """Test the retrieval of task list"""
        self.authenticate()  # Ensure the user is authenticated

        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_update_todo(self):
        """Test the updation of the task"""

        self.authenticate()  # Ensure the user is authenticated
        updated_data = {
            "title": "Updated Task",
            "description": "Updated Desc",
            "status": "COMPLETED",
            "tags": "Django, Testing, API",
        }
        response = self.client.put(self.todo_url, updated_data, format="json")
        # print(response.content)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Task")

    def test_delete_todo(self):
        """Test the deletion of the todo task"""

        self.authenticate()  # Ensure the user is authenticated
        response = self.client.delete(self.todo_url)
        # print(response.content)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())
