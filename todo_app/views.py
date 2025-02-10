from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from rest_framework.exceptions import PermissionDenied

# #create a to-do item
# class TodoCreateView(generics.CreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [AllowAny]

# #retrieve a single to-do item
# class TodoDetailView(generics.RetrieveAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [AllowAny]


# Retrieve single to-do item with all methods permission like GET, POST, PUT, DELETE
class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure a user can only retrieve their own tasks."""
        return Todo.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the owner of the task can update it"""
        todo = self.get_object()
        if todo.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this task.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the owner can delete the tasks"""
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have access to delete this task.")
        instance.delete()


# #retrieve all to-do items
# class TodoListView(generics.ListAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [AllowAny]


# Retrieve all to-do items with all methods permission like GET, POST, PUT, DELETE
class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# #Update a to-do item
# class TodoUpdateView(generics.UpdateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [AllowAny]

# #Delete a to-do item
# class TodoDeleteView(generics.DestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     # authentication_classes = [BasicAuthentication]
#     # permission_classes = [AllowAny]


class UserRegistrationView(generics.CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
