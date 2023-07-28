"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User

class UserView(ViewSet):
    """Users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all users
        Returns:
            Response -- JSON serialized list of users
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """CREATE User"""

        user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            profile_image_url=request.data["profile_image_url"],
            email=request.data["email"],
            uid=request.data["uid"],
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a user
        
        Returns -- Empty body with 204 status code
        """
        user = User.objects.get(pk=pk)
        user.first_name=request.data["first_name"]
        user.last_name=request.data["last_name"]
        user.profile_image_url=request.data["profile_image_url"]
        user.email=request.data["email"]

        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare users"""

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'profile_image_url',
                  'email',
                  'uid')
        depth = 1
