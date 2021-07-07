from stream_chat import StreamChat

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from .initialize_rooms import initialize_rooms

client = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_SECRET_KEY)
initialize_rooms(client)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStreamToken(request):
    token = client.create_token(str(request.user.id))

    return Response({'token': token})