"""
Как пользователь, я хочу получить конкретную информацию о конкретном пользователе.

Сценарий:

Когда я отправляю GET-запрос на /api/v1/users/<username>/, я получаю ответ со статусом 200 OK.

И ответ включает следующие данные о выводе:

username:
    • Проверка минимальной и максимальной длины.
    • Проверка на запрещенные символы, такие как пробелы, специальные символы.

first_name:
last_name:
    • Проверка минимальной и максимальной длины.
    • Проверка, чтобы не содержались цифры и запрещенные символы.

email:
    • Проверка на правильные форматы электронной почты.
    • Проверка длины адреса электронной почты

phone:
    • Проверка на правильные форматы телефонных номеров.
    • Проверка минимальной и максимальной длины.

position:
    • Проверка на правильные значения ввода.
    • Проверка минимальной и максимальной длины.

project:
    • Проверка на правильные названия проектов.
    • Проверка минимальной и максимальной длины.

Получение вывода с некорректным username. Username: aaaaaaaaa
Когда я отправляю GET-запрос на /api/v1/users/aaaaaaaaa/, я получаю ответ со статусом "404 Not Found",
и ответ содержит сообщение: "Не могу найти пользователя <aaaaaaaaa>"
"""

from django.test import TestCase
from rest_framework import status
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.projects.models import Project
from apps.users.models import User


class GetCurrentUserSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Project.objects.all()
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'position', 'project')


class GetCurrentUserAPIView(APIView):

    def get_object(self, username):
        return User.objects.filter(username=username).first()

    def get(self, request: Request, username: str) -> Response:
        user = self.get_object(username)

        if not user:
            return Response(
                data={'detail': f'Пользователя {username} не существует'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetCurrentUserSerializer(user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class GetSomeUserInfoTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Project',
            description='Test project description'
        )

        self.user = User.objects.create(
            username='newuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            phone='+1234567890',
            position='DESIGNER',
            project=self.project
        )

    def tearDown(self):
        User.objects.all().delete()
        Project.objects.all().delete()

    def test_get_some_user_info(self):
        response = self.client.get('/api/v1/users/newuser/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

        expected_fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'position',
            'project'
        ]

        for field in expected_fields:
            self.assertIn(field, response.data)

        self._check_username(response.data['username'])
        self._check_name(response.data['first_name'], 'first_name')
        self._check_name(response.data['last_name'], 'last_name')
        self._check_email(response.data['email'])
        self._check_phone(response.data['phone'])
        self._check_position(response.data['position'])
        self._check_project(response.data['project'])

    def test_get_user_info_invalid_username(self):
        invalid_username = 'aaaaaaaaa'
        response = self.client.get(f'/api/v1/users/{invalid_username}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(f'Пользователя {invalid_username} не существует', response.data['detail'])
        self.assertIn(invalid_username, response.data['detail'])

    def _check_username(self, username):
        self.assertGreaterEqual(len(username), 3, "Username is too short")
        self.assertLessEqual(len(username), 50, "Username is too long")
        forbidden_symbols = set(' !@#$%^&*()+=[]{}|\\:;"\'<>,.?/')
        self.assertFalse(any(char in forbidden_symbols for char in username), "Username contains forbidden symbols")

    def _check_name(self, name, field_name):
        self.assertGreaterEqual(len(name), 3, f"{field_name} is too short")
        self.assertLessEqual(len(name), 40, f"{field_name} is too long")
        self.assertRegex(name, r'^[a-zA-Z]+$', f"{field_name} contains non-alphabetic characters")

    def _check_email(self, email):
        self.assertRegex(email, r'^[\w\.-]+@[\w\.-]+\.\w+$', "Email format is invalid")
        self.assertLessEqual(len(email), 254, "Email is too long")

    def _check_phone(self, phone):
        self.assertRegex(phone, r'^\+?[\d\s\-]+$', "Phone number format is invalid")
        self.assertGreaterEqual(len(phone), 7, "Phone number is too short")
        self.assertLessEqual(len(phone), 75, "Phone number is too long")

    def _check_position(self, position):
        self.assertRegex(position, r'^[a-zA-Z0-9\s]+$', "Position contains invalid characters")
        self.assertGreaterEqual(len(position), 1, "Position is empty")
        self.assertLessEqual(len(position), 100, "Position is too long")

    def _check_project(self, project):
        self.assertRegex(project, r'^[a-zA-Z0-9\s]+$', "Project contains invalid characters")
        self.assertGreaterEqual(len(project), 1, "Project is empty")
        self.assertLessEqual(len(project), 100, "Project is too long")
