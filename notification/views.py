from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ExpoTokenSerializer
from .models import ExpoToken

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def storeNotificationTokenView(request):
    serializer = ExpoTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        token, created = ExpoToken.objects.get_or_create(user=request.user, token=data['token'])

        return Response({'msg': 'Token stored'})
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)