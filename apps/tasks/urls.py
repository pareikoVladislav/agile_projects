from django.urls import path

from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView
from apps.tasks.views.task_views import TasksListAPIView, TaskDetailAPIView


urlpatterns = [
    path('', TasksListAPIView.as_view()),
    path('<int:pk>/', TaskDetailAPIView.as_view()),
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
]
