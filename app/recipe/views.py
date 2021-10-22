from rest_framework import permissions, authentication, mixins, viewsets

from . import serializers
from .models import Tag


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('-name')
