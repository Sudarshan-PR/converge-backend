from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializer import UserRegisterSerializer

from home.models import Profile

class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Create empty profile for the given user
            profile = Profile(user=user)
            profile.save()

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response({'Error': "Something is wrong in the server. Please try again"}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
