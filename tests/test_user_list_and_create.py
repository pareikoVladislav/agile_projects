from django.test import TestCase

from rest_framework import status
from apps.users.models import User


class UserListAndNewRegister(TestCase):

    def setUp(self):
        users = [
            User(
                username='newuser',
                first_name='Test',
                last_name='User',
                email='testuser@example.com',
                password='password123',
                position='Designer'
            )
        ]

        User.objects.bulk_create(users)

    def tearDown(self):
        User.objects.all().delete()

    def test_get_users_list(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        expected_fields = ['first_name', 'last_name', 'email', 'position']

        for user in response.data:
            self.assertIsInstance(user, dict)

            for field in expected_fields:
                self.assertIn(field, user)
                self.assertIsInstance(user[field], str)
                if field == 'position':
                    self.assertRegex(user['position'], '^[A-Za-z ]{1,20}$')
                else:
                    self.assertRegex(user[field], '^[A-Za-z ]{1,40}$' if field != 'email' else '^[A-Za-z0-9@.]+$')

    def test_register_new_user(self):
        data = {
            'username': 'validuser',
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@example.com',
            'position': 'CEO',
            'password': 'Password123#',
            're_password': 'Password123#',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(User.objects.get(email='validuser@example.com').username, data['username'])

    def test_register_user_with_different_password(self):
        data = {
            'username': 'validuser',
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'validuser@example.com',
            'position': 'CEO',
            'password': 'Password123#',
            're_password': 'Password124#',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'], ['Password must be same.'])

    def test_register_user_invalid_username(self):
        data = {
            'username': 'invalid user',
            'first_name': 'Invalid',
            'last_name': 'User',
            'email': 'invaliduser@example.com',
            'position': 'CEO',
            'password': 'Password123#',
            're_password': 'Password123#',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_name', response.data)  # Check 'user_name' instead of 'username'
        self.assertEqual(response.data['user_name'],
                         ['The username must be alphanumeric characters or have only _ . symbols.'])

    def test_register_user_invalid_first_name(self):
        data = {
            'username': 'validuser2',
            'first_name': 'Invalid1',
            'last_name': 'User',
            'email': 'invalidfirstname@example.com',
            'position': 'CEO',
            'password': 'Password123#',
            're_password': 'Password123#',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertEqual(response.data['first_name'], ['The first_name must be alphabet characters.'])

    def test_register_user_invalid_last_name(self):
        data = {
            'username': 'validuser3',
            'first_name': 'Valid',
            'last_name': 'User1',
            'email': 'invalidlastname@example.com',
            'position': 'CEO',
            'password': 'Password123#',
            're_password': 'Password123#',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.data)
        self.assertEqual(response.data['last_name'], ['The last_name must be alphabet characters.'])

    def test_register_user_invalid_password(self):
        data = {
            'username': 'validuser4',
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'invalidpassword@example.com',
            'position': 'CEO',
            'password': 'qwerty',
            're_password': 'qwerty',
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertTrue(any('password' in error.lower() for error in response.data['password']))
