from rest_framework import generics, permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
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


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return authenticated user
        In the usual mode, we should declare queryset and the request should have pk argument to get the desired model
        We don't to send pk argument to retrieve the user object,
        instead we want to return the user that send the request.
        get_object has the job to retrieve the user object, so we override it and just return the use
        """
        return self.request.user
