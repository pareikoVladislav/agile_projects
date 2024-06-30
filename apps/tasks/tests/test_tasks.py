from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from apps.projects.models import Project
from apps.tasks.models import Tag, Task
from apps.users.models import User
from apps.tasks.choices.priorities import Priorities
from apps.tasks.serializers.tasks_serializers import CreateUpdateTaskSerializer


class CreateTasksTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description="Test description for the test project name for the Unit tests."
        )
        self.tag1 = Tag.objects.create(id=1, name='Backend')
        self.tag2 = Tag.objects.create(id=2, name='DevOPS')
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='uer',
            email='user@example.com',
            position="PRODUCT_OWNER",
            password='test'
        )

    def test_create_task_with_valid_data(self):
        valid_data = {
            "name": "Valid Test Task Name",
            "description": "Test description for the test task description with more than 50 chars.",
            "priority": Priorities.HIGH[0],
            "project": self.project.name,
            "tags": [1, 2],
            "deadline": timezone.now() + timedelta(days=10),
        }

        serializer = CreateUpdateTaskSerializer(data=valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.validated_data['name'], str)
        self.assertIsInstance(serializer.validated_data['description'], str)
        self.assertIsInstance(serializer.validated_data['priority'], int)
        self.assertIsInstance(serializer.validated_data['project'], Project)
        self.assertIsInstance(serializer.validated_data['tags'], list)

        for tag in serializer.validated_data['tags']:
            self.assertIsInstance(tag, Tag)

        self.assertIsInstance(serializer.validated_data['deadline'], timezone.datetime)

    def test_create_task_with_short_task_name(self):
        invalid_data = {
            "name": "Short",
            "description": "Test description for the test task description with more than 50 chars.",
            "priority": Priorities.HIGH[0],
            "project": self.project.name,
            "tags": [1, 2],
            "deadline": timezone.now() + timedelta(days=10),
        }

        serializer = CreateUpdateTaskSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], 'Name must be at least 10 characters')

    def test_create_task_with_bad_priority(self):
        invalid_data = {
            "name": "Valid Test Task Name",
            "description": "Test description for the test task description with more than 50 chars.",
            "priority": 99,
            "project": self.project.name,
            "tags": [1, 2],
            "deadline": timezone.now() + timedelta(days=10),
        }

        serializer = CreateUpdateTaskSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('priority', serializer.errors)
        self.assertEqual(
            serializer.errors['priority'][0],
            '"99" is not a valid choice.'
        )

    def test_create_task_with_deadline_in_past(self):
        invalid_data = {
            "name": "Valid Test Task Name",
            "description": "Test description for the test task description with more than 50 chars.",
            "priority": Priorities.HIGH[0],
            "project": self.project.name,
            "tags": [1, 2],
            "deadline": timezone.now() - timedelta(days=1),
        }

        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('deadline', serializer.errors)
        self.assertEqual(
            serializer.errors['deadline'][0],
            'Deadline time can not be in past'
        )
