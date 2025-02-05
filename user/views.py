from rest_framework.response import Response
from rest_framework import status

from user.models import User
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView


class UserList(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            return Response({'user': UserSerializer(user).data, 'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
