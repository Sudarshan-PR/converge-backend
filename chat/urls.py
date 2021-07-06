from django.urls import path

from .views import getStreamToken

urlpatterns = [
    path("token", getStreamToken, name="stream-token"),
]