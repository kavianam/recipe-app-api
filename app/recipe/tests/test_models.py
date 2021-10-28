from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from recipe.models import Tag, Ingredient, Recipe
from recipe import models


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


class TestIngredient(TestCase):
    """Test the Ingredient model"""

    def setUp(self) -> None:
        self.client = APIClient

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = Ingredient.objects.create(
            name='Sugar',
            user=create_user()
        )

        self.assertEqual(str(ingredient), ingredient.name)


class TestRecipe(TestCase):
    """Test """

    def setUp(self) -> None:
        self.client = APIClient

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = Recipe.objects.create(
            user=create_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4', return_value='test_uuid')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'my_image.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
