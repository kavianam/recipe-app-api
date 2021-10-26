from rest_framework import serializers

from .models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    ingredients = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all(),
        many=True
    )
    tags = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all(),
        many=True
    )
    # We could also use PrimaryKeyRelatedField, but we wanted to show the ingredients name instead of their id
    # ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'ingredients', 'tags', 'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
