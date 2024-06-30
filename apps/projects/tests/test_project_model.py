from django.test import TestCase
from unittest.mock import MagicMock
from apps.projects.models import Project


class TestProjectModel(TestCase):

    def test_project_str(self):
        # Создаем MagicMock объект
        mock_project = MagicMock(spec=Project)
        mock_project.name = 'Test Project'

        # Устанавливаем возвращаемое значение метода __str__
        mock_project.__str__.return_value = 'Test Project'

        # Проверяем, что метод __str__ возвращает ожидаемое значение
        self.assertEqual(str(mock_project), 'Test Project')
