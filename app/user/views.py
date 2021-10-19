from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user.
    If we didn't create our custom user, we could have just put ObtainAuthToken in the urls.
    """
    serializer_class = AuthTokenSerializer
    # This will allow us to view this view in the browser and send request in it
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
