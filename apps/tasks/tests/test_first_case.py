from django.test import TestCase


class FirstCaseTestCase(TestCase):
    def test_first_case(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to my site!')
