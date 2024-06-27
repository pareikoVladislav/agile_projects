import json

from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response

from apps.tasks.models import Tag


class TagsListTestCase(TestCase):
    # def setUpClass(cls):
    #     ...
    # def tearDownClass(cls):
    #     ...

    @classmethod
    def setUpClass(cls):
        tags = [
            Tag(name='Backend'),
            Tag(name='Frontend'),
            Tag(name='DevOPS'),
            Tag(name='Testing'),
            Tag(name='Design'),
            Tag(name='Data Science'),
            Tag(name='Data Analytics'),
            Tag(name='Machine Learning'),
        ]

        Tag.objects.bulk_create(tags)

    @classmethod
    def tearDownClass(cls):
        Tag.objects.all().delete()

    def test_get_all_tags(self):
        response = self.client.get('/api/v1/tasks/tags/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, Response)

        # проверка данных и их типов
        self.assertIsInstance(response.data, list)

        for tag in response.data:
            self.assertIsInstance(tag, dict)
            self.assertIn('name', tag)
            self.assertIsInstance(tag['name'], str)
            self.assertRegex(tag['name'], '^[a-zA-Z ]{4,20}$')

    def test_create_new_valid_tag(self):
        data = {"name": "Test Tag"}

        response = self.client.post('/api/v1/tasks/tags/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(Tag.objects.get(name='Test Tag').name, data['name'])

    def test_create_new_invalid_tag(self):
        data = {"name": "QA"}
        response = self.client.post('/api/v1/tasks/tags/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_tag_with_empty_data(self):
        data = {}

        response = self.client.post('/api/v1/tasks/tags/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_tag_with_bad_data_type(self):
        data = {"name": [(2, 4, 5), (2, 3, 4)]}

        raw_data = json.dumps(data)

        response = self.client.post(
            '/api/v1/tasks/tags/',
            data=raw_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveTagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(id=1, name='DevOPS')

    def tearDown(self):
        Tag.objects.all().delete()

    def test_get_object_by_id(self):  # DevOPS
        response = self.client.get('/api/v1/tasks/tags/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], 'DevOPS')

    def test_get_object_by_non_existent_id(self):
        response = self.client.get('/api/v1/tasks/tags/999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTagTestCase(TestCase):

    def setUp(self):
        Tag.objects.create(id=1, name='DevOPS')

    def test_update_tag_with_valid_data(self):
        data_to_update = json.dumps({"name": "TEST DEVOPS"})

        response = self.client.put(
            '/api/v1/tasks/tags/1/',
            data=data_to_update,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['name'], 'TEST DEVOPS')

    def test_update_tag_with_invalid_data(self):
        data_to_update = {"name": [(2, 4, 5), (2, 3, 4)]}

        raw_data = json.dumps(data_to_update)

        response = self.client.put(
            '/api/v1/tasks/tags/1/',
            data=raw_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name='Backend')

    def test_delete_tag_by_id(self):
        response = self.client.delete('/api/v1/tasks/tags/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(response.data, {
            "message": "Successfully deleted"
        })


class EmptyTagsListTestCase(TestCase):

    def test_get_empty_list_of_tags(self):
        response = self.client.get('/api/v1/tasks/tags/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)
