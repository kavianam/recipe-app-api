from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


def create_user(email='test@test.com', password='Test1234'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientTests(TestCase):
    """Test the publicly available ingredient API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the private ingredient API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user('kavianam@gmail.com', 'Test1234')
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(name='Sugar', user=self.user)
        Ingredient.objects.create(name='Salt', user=self.user)

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for the authenticated user are returned"""
        ingredients = Ingredient.objects.create(name='Sugar', user=self.user)
        Ingredient.objects.create(name='Pepper', user=create_user())

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)

    def test_create_ingredient_successful(self):
        """Test create a new ingredient"""
        payload = {
            'name': 'sugar',
            'user': self.user
        }
        res = self.client.post(INGREDIENT_URL, payload)

        ingredient = Ingredient.objects.filter(
            name=payload['name'],
            user=self.user
        )

        self.assertTrue(ingredient.exists())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {
            'name': '',
            'user': self.user
        }
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
