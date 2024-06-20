from django.urls import path

from apps.projects.views.project_files_views import (
    ProjectFileListGenericView,
    ProjectFileDetailGenericView
)
from apps.projects.views.project_views import ProjectListAPIView, ProjectDetailAPIView


urlpatterns = [
    path('', ProjectListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('files/', ProjectFileListGenericView.as_view()),
    path('files/<int:file_id>/', ProjectFileDetailGenericView.as_view())
]
