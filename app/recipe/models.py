import uuid
import os

from django.db import models
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image. Images will be stored in this path relative to the MEDIA_ROOT."""
    extension = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads', 'recipe', new_filename)


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe objects"""
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    time_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
