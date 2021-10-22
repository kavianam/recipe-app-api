from rest_framework import permissions, authentication, mixins, viewsets

from . import serializers
from .models import Tag, Ingredient


class TagViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Assign the user to the tag user. We can also override the create method of the TagSerializer"""
        serializer.save(user=self.request.user)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Manage Ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Assign the user to the ingredient obj. We can also override the create method of the IngredientSerializer"""
        serializer.save(user=self.request.user)
