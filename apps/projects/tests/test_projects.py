from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.projects.models import Project
from apps.projects.serializers.project_serializers import (
    AllProjectsSerializer, ProjectDetailSerializer,
)
from apps.projects.views.project_views import ProjectListAPIView, ProjectDetailAPIView


class TestRetrieveUpdateProjectAPIView(APITestCase):
    fixtures = ['apps/fixtures/projects_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.mock_project = Project.objects.create(
            name='Test Project',
            description='Description for test project'
        )
        self.project = Project.objects.get(pk=1)
        self.url = reverse('project-detail', kwargs={'pk': 1})

    @patch.object(ProjectDetailAPIView, 'get_object')
    def test_update_project(self, mock_get_object):
        mock_get_object.return_value = self.mock_project
        data = {
            'name': 'Updated Project',
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.mock_project.name, 'Updated Project')

    def test_delete_project(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Project deleted successfully'})

        # Проверка, что проект был удален из базы данных
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_get_project(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ProjectDetailSerializer(self.project)
        self.assertEqual(response.data, serializer.data)
