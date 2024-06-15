from django.urls import path

from apps.projects.views.project_views import (
    ProjectsListAPIView,
    ProjectDetailAPIView
)
from apps.projects.views.project_file_views import (
    ProjectFileListGenericView,
)

urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('files/', ProjectFileListGenericView.as_view()),
]
