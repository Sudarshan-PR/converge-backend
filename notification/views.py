from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ExpoTokenSerializer
from .models import ExpoToken

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def storeNotificationTokenView(request):
    serializer = ExpoTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        token = ExpoToken(user=request.user, token=data['token'])
        token.save()
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)