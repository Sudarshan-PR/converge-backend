"""
ASGI config for Converge project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.getenv("ENV") == "Heroku":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Converge.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Converge.dev_settings')

application = get_asgi_application()