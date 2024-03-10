from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from server.settings import SIMPLE_JWT
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework import permissions, status, views





class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # The request.user property will have the user instance for authenticated requests
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
