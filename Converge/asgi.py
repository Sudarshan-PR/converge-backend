"""
ASGI config for Converge project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# import chat.router
from . import router

if os.getenv("ENV") == "Heroku":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Converge.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Converge.dev_settings')

application = ProtocolTypeRouter({
    # Handling HTTP Applications
    "http": get_asgi_application(),

    # Handling Websockets
    "websocket": AuthMiddlewareStack(
        URLRouter(
            router.websocket_urlpatterns,
        )
    ),

})