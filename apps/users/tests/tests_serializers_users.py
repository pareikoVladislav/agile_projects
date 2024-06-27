from django.test import TestCase

from apps.users.choices.positions import Positions
from apps.users.serializers import RegisterUserSerializer


class RegisterUserSerializerTests(TestCase):

    def test_create_user_valid_data(self):
        valid_data = {
            "username": "solodkov_test_user_100",
            "first_name": "Edwardson",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.validated_data['username'], str)
        self.assertIsInstance(serializer.validated_data['first_name'], str)
        self.assertIsInstance(serializer.validated_data['last_name'], str)
        self.assertIsInstance(serializer.validated_data['email'], str)
        self.assertIsInstance(serializer.validated_data['position'], str)
        self.assertIsInstance(serializer.validated_data['password'], str)
        self.assertIsInstance(serializer.validated_data['re_password'], str)

    def test_create_user_empty_data(self):
        empty_data = {}

        serializer = RegisterUserSerializer(data=empty_data)

        self.assertFalse(serializer.is_valid())

        required_field = 'This field is required.'

        self.assertEqual(str(serializer.errors['username'][0]), required_field)
        self.assertEqual(str(serializer.errors['first_name'][0]), required_field)
        self.assertEqual(str(serializer.errors['last_name'][0]), required_field)
        self.assertEqual(str(serializer.errors['email'][0]), required_field)
        self.assertEqual(str(serializer.errors['position'][0]), required_field)
        self.assertEqual(str(serializer.errors['password'][0]), required_field)
        self.assertEqual(str(serializer.errors['re_password'][0]), required_field)

    def test_create_user_invalid_username(self):
        incorrect_username_data = {
            "username": "solodkov test_invalid?user_name",
            "first_name": 'Antony',
            "last_name": 'Johnson',
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_username_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # TODO: Change field name in the ValidationError from 'user_name' to 'username' -> apps/users/serializers.py:48
        self.assertEqual(
            str(serializer.errors['user_name'][0]),
            'The username must be alphanumeric characters or have only _ . symbols.'
        )

    def test_create_user_invalid_first_name_type(self):
        incorrect_name_type_data = {
            "username": "solodkov_test_invalid_user_name",
            "first_name": 123,
            "last_name": 'Johnson',
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_name_type_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['first_name'][0]),
            'The first_name must be alphabet characters.'
        )

    def test_create_user_invalid_first_name_length(self):
        incorrect_name_length_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Afantasticmagicalwonderfulincredibleamazing",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_name_length_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['first_name'][0]),
            'Ensure this field has no more than 40 characters.'
        )

    def test_create_user_invalid_last_name_type(self):
        incorrect_name_type_data = {
            "username": "solodkov_test_invalid_user_name",
            "first_name": 'Antony',
            "last_name": 123,
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_name_type_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['last_name'][0]),
            'The last_name must be alphabet characters.'
        )

    def test_create_user_invalid_last_name_length(self):
        incorrect_name_length_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Afantasticmagicalwonderfulincredibleamazing",
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_name_length_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['last_name'][0]),
            'Ensure this field has no more than 40 characters.'
        )

    def test_create_user_email_without_domain(self):
        email_wo_domain_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn.edward.johnson",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=email_wo_domain_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['email'][0]),
            'Enter a valid email address.'
        )

    def test_create_user_email_with_invalid_domain(self):
        email_invalid_domain_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=email_invalid_domain_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['email'][0]),
            'Enter a valid email address.'
        )

    def test_create_user_email_with_invalid_local_part(self):
        email_invalid_local_part_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn edward johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=email_invalid_local_part_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['email'][0]),
            'Enter a valid email address.'
        )

    def test_create_user_incorrect_position_value(self):
        incorrect_position_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich.de",
            "position": 'TEST',
            "password": "Great123",
            "re_password": "Great123",
        }

        serializer = RegisterUserSerializer(data=incorrect_position_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['position'][0]),
            '"TEST" is not a valid choice.'
        )

    def test_create_user_common_pass(self):
        incorrect_position_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "qwerty",
            "re_password": "qwerty",
        }

        serializer = RegisterUserSerializer(data=incorrect_position_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['password'][0]),
            'This password is too short. It must contain at least 8 characters.'
        )

    def test_create_user_not_same_passwords(self):
        incorrect_position_data = {
            "username": "solodkov_test_long_user_name",
            "first_name": "Antony",
            "last_name": "Johnson",
            "email": "jn.edward.johnson@ich.de",
            "position": Positions.QA,
            "password": "Great123",
            "re_password": "Great125",
        }

        serializer = RegisterUserSerializer(data=incorrect_position_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(
            str(serializer.errors['password'][0]),
            'Password must be same.'
        )

