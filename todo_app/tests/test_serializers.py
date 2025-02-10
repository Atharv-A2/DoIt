from django.test import TestCase
from todo_app.serializers import TodoSerializer


class TodoSerializerTest(TestCase):

    def test_valid_serializer(self):
        """Test if the data is serialized correctly"""
        valid_data = {
            "title": "learn DRF",
            "description": "Study Django Rest Framework",
            "status": "WORKING",
        }
        serializer = TodoSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        """Test serializer with invalid data (missing title)"""
        invalid_data = {"description": "Missing Title Field"}
        serializer = TodoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
