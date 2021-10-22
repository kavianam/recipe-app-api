from django.urls import path, include

from rest_framework import routers

from .views import TagViewSet, IngredientViewSet


app_name = 'recipe'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
# basename is responsible for the basename of the view names. For example here we have tag-list view

urlpatterns = [
    path('', include(router.urls)),
]
