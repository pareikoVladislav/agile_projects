from django.test import TestCase

from apps.tasks.models import Tag


class TagsListTestCase(TestCase):
    fixtures = ['apps/fixtures/tags_fixture.json']

    def test_tags_count(self):
        self.assertEqual(Tag.objects.count(), 8)

    def test_tags_name_data_type(self):
        tags = Tag.objects.all()
        for tag in tags:
            self.assertIsInstance(tag.name, str)
