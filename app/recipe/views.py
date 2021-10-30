from rest_framework import permissions, authentication, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .models import Tag, Ingredient, Recipe


class BaseRecipeAttrViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """Base viewSet for user owned recipe attributes"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = self.queryset
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))
        if assigned_only:
            queryset = queryset.filter(recipes__isnull=False)
            # Django return one item for every related items means for every
            # it may return duplicate obj that we can remove them by distinct.
        return queryset.filter(user=self.request.user)\
                       .order_by('-name')\
                       .distinct()

    def perform_create(self, serializer):
        """Assign the user to the obj. We can also override the create method of the Serializer"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


def params_to_int(qs):
    """Convert a list of string IDs to a list of ints"""
    return [int(str_id) for str_id in qs.split(',')]


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        recipes = self.queryset
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        if tags:
            tag_ids = params_to_int(tags)
            recipes = recipes.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = params_to_int(ingredients)
            recipes = recipes.filter(ingredients__id__in=ingredient_ids)

        return recipes.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            # Actions are just the method of the view.
            # Possible actions are: retrieve, list, create, destroy or any user writable methods like upload_image
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """create a new recipe and apply current user to it"""
        serializer.save(user=self.request.user)

    @action(methods=['post'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(
            instance=recipe,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
