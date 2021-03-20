from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserRegisterSerializer

class UserRegisterView(APIView):
    def post(self, request, format='json'):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.data, status=502)

        return Response(serializer.data, status=400)
            
