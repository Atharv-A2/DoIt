from django.urls import path
from .views import TodoRetrieveUpdateDestroyView, TodoListCreateView
from .views import UserRegistrationView

urlpatterns = [
    path("api/todo/", TodoListCreateView.as_view(), name="todo-list-create"),
    # path('api/todo/create/', TodoCreateView.as_view(), name="todo-create"),
    path(
        "api/todo/<int:pk>/",
        TodoRetrieveUpdateDestroyView.as_view(),
        name="todo-detail",
    ),
    # path('api/todo/<int:pk>/update/', TodoUpdateView.as_view(), name="todo-update"),
    # path('api/todo/<int:pk>/delete/', TodoDeleteView.as_view(), name="todo-delete"),
    path("api/register/", UserRegistrationView.as_view(), name="register"),
]
