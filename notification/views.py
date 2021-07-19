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
            token = ExpoToken.objects.get(user=request.user, token=data['token'])
            # Set token as active
            token.active = True
            token.save()
        except ObjectDoesNotExist:
            ExpoToken.objects.create(user=request.user, token=data['token'])
        except MultipleObjectsReturned:
            pass
        finally:
            return Response({'msg': 'Token stored'})
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsetNotificationTokenView(request):
    serializer = ExpoTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data

        try:
            token = ExpoToken.objects.get(user=request.user, token=data['token'])
            token.active = False
            token.save()
        except:
            pass
        finally:
            return Response({'msg': f'Deviced set inactive to user {request.user.email}'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotificationView(request):
    notification = UserNotifications.objects.filter(user=request.user).order_by('-created_at')
    serializer = UserNotificationsSerializer(notification, many=True)

    if not(serializer):
        data = [{
            "event": "Welcome to Converge!",
            "msg": "You dont seem to have any notifications yet!",
            "created-at": request.user.data_joined.isoformat()
        }]
    else:
        data = serializer.data

    return Response(data)