from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ExpoTokenSerializer, UserNotificationsSerializer
from .models import ExpoToken, UserNotifications

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def storeNotificationTokenView(request):
    serializer = ExpoTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data

        try:
            ExpoToken.objects.get(user=request.user, token=data['token'])
        except ObjectDoesNotExist:
            ExpoToken.objects.create(user=request.user, token=data['token'])
        except MultipleObjectsReturned:
            pass

        return Response({'msg': 'Token stored'})
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotificationView(request):
    notification = UserNotifications.objects.filter(user=request.user)
    serializer = UserNotificationsSerializer(notification, many=True)

    return Response(serializer.data)