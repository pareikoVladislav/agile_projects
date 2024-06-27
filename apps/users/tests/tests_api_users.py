from django.test import TestCase

from rest_framework import status
from rest_framework.response import Response

from apps.projects.models import Project
from apps.users.choices.positions import Positions
from apps.users.models import User


class ApiUsersListTestCase(TestCase):
    fields_types = (
        # в используемом сериализаторе отсутствует поле username,
        # поэтому этого поля нету в списке для проверки
        ('first_name', str),
        ('last_name', str),
        ('email', str),
        ('position', str)
    )

    def setUp(self):
        users = [
            User(
                username='solodkov_test_user_1',
                first_name='John',
                last_name='Doe',
                email='john.doe@ich.de',
                position=Positions.QA
            ),
            User(
                username='solodkov_test_user_2',
                first_name='Charlie',
                last_name='Garcia',
                email='charlie.garcia@ich.de',
                position=Positions.DESIGNER
            ),
            User(
                username='solodkov_test_user_3',
                first_name='Alice',
                last_name='Smith',
                email='alice.smith@ich.de',
                position=Positions.PROJECT_OWNER
            ),
            User(
                username='solodkov_test_user_4',
                first_name='George',
                last_name='Jones',
                email='george.jones@ich.de',
                position=Positions.CTO
            ),
            User(
                username='solodkov_test_user_5',
                first_name='Charlie',
                last_name='Williams',
                email='charlie.williams@ich.de',
                position=Positions.QA
            ),
            User(
                username='solodkov_test_user_6',
                first_name='Bob',
                last_name='Rodriguez',
                email='bob.rodriguez@ich.de',
                position=Positions.DESIGNER
            ),
            User(
                username='solodkov_test_user_7',
                first_name='Fiona',
                last_name='Brown',
                email='fiona.brown@ich.de',
                position=Positions.PROGRAMMER
            ),
            User(
                username='solodkov_test_user_8',
                first_name='Hannah',
                last_name='Davis',
                email='hannah.davis@ich.de',
                position=Positions.PROJECT_MANAGER
            ),
            User(
                username='solodkov_test_user_9',
                first_name='Edward',
                last_name='Johnson',
                email='edward.johnson@ich.de',
                position=Positions.CEO
            ),
            User(
                username='solodkov_test_user_10',
                first_name='John',
                last_name='Miller',
                email='john.miller@ich.de',
                position=Positions.PRODUCT_OWNER
            )

        ]
        User.objects.bulk_create(users)

    def tearDown(self):
        User.objects.all().delete()

    def assertDictValuesTypes(self, dictionary, fields_n_types):
        for key, instance in fields_n_types:
            with self.subTest(key=key, value=dictionary[key], instance=instance):
                self.assertIsInstance(dictionary[key], instance)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, Response)

        self.assertIsInstance(response.data, list)

        for user in response.data:
            self.assertIsInstance(user, dict)

            # тут фактическая проверка и на существование ключей в словаре
            # и на соответствие типа данных
            self.assertDictValuesTypes(user, self.fields_types)


class ApiUsersEmptyListTestCase(TestCase):
    def test_empty_list(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)


class ApiUserCreateTestCase(TestCase):

    def test_create_valid_user(self):
        data = {
            "username": "solodkov_test_user_retrieve_1",
            "first_name": "Retrieve",
            "last_name": "Checking",
            "email": "retrieve.checking@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        # TODO: Change response status code in the view from 200 to 201
        #  BUG: POST Request to '/api/v1/users/register/' returns status 200 instead of 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)

        self.assertEqual(User.objects.get(username=data['username']).username, data['username'])
        self.assertEqual(User.objects.get(username=data['username']).first_name, data['first_name'])
        self.assertEqual(User.objects.get(username=data['username']).last_name, data['last_name'])
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertEqual(User.objects.get(username=data['username']).position, data['position'].value)

    def test_create_user_empty_data(self):
        data = {}
        response = self.client.post('/api/v1/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)


class ApiUserRetrieveTestCase(TestCase):
    fields_types = (
        ('username', str),
        ('first_name', str),
        ('last_name', str),
        ('email', str),
        ('position', str),
        ('phone', str),
        ('project', int),
    )

    def assertDictValuesTypes(self, dictionary, fields_n_types):
        for key, instance in fields_n_types:
            with self.subTest(key=key, value=dictionary[key], instance=instance):
                self.assertIsInstance(dictionary[key], instance)

    def setUp(self):
        proj = Project.objects.create(
            id=1,
            name="SAPHYR INC",
            description="This is a high quelity platform to provide financial predictions to your business."
        )
        self.user_data = {
            "id": 1,
            "username": 'solodkov_test_user_retrieve_1',
            "first_name": 'Retrieve',
            "last_name": 'Checking',
            "email": 'retrieve.checking@ich.de',
            "phone": '+4912309609483',
            "position": Positions.CEO,
            "project": proj
        }

        User.objects.create(**self.user_data)

    def tearDown(self):
        Project.objects.all().delete()
        User.objects.all().delete()

    def test_retrieve_user_by_id(self):
        response = self.client.get('/api/v1/users/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.data, dict)

        self.assertDictValuesTypes(response.data, self.fields_types)

        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['last_name'], self.user_data['last_name'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['phone'], self.user_data['phone'])
        self.assertEqual(response.data['position'], self.user_data['position'].value)
        self.assertEqual(response.data['project'], self.user_data['project'].id)

    def test_retrieve_non_existing_user(self):
        response = self.client.get('/api/v1/users/999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(str(response.data['detail']), 'No User matches the given query.')
