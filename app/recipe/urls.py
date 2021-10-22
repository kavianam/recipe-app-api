from django.urls import path, include

from rest_framework import routers

from .views import TagViewSet


app_name = 'recipe'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
# basename is responsible for the basename of the view names. For example here we have tag-list view

urlpatterns = [
    path('', include(router.urls)),
]
