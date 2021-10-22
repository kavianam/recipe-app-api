from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from ..models import Tag
# from recipe.models import Tag


def create_user(email='test@test.com', password='Test1234'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class TestTag(TestCase):
    """Test the tag model"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=create_user(),
            name='vegan'
        )
        self.assertEqual(str(tag), tag.name)
