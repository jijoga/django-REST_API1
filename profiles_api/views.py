from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters #For searching objects
from rest_framework.authtoken.views import ObtainAuthToken #For atoken authorization
from rest_framework.settings import api_settings #For atoken authorization
from rest_framework.permissions import IsAuthenticated

from profiles_api import models
from profiles_api import serializers
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""
    serializer_class=serializers.HelloSerializer
    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            ) #The status code can simply be passed as an integer. But passing it like this gives an idea of the error

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    #For searching the objects
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',) #allows to search by name and email fields

#This clsss is for authorizing the user by token
class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   #Below code is to make this visible in the browsable API. For all other base classes this code is available by default. But for ObtainAuthToken, we need to give it manualy to be visible in browsable API
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    #Below permissio_class code says if the user is authenticated, then he can edit/read his own status feed.
    permission_classes = (
        permissions.UpdateOwnStatus,IsAuthenticated
    )
    #When a request is made to the ModelViewSet, the request is passed to serializer_class we defined in it and data is validated_
    #and then the serializer.save() is called automatically because it is a ModelViewSet. This saves the model parameters to DB.
    #If we need to alter the way the model is saved, we should define it in perform_create() function which is  builtin function of DRF
    #and define the save in it. Here we use it since the user_profile is defined as read_only and DRF will not automayically save it
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
