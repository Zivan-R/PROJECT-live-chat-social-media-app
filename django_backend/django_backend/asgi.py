"""
ASGI config for django_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

# Solved the django.core.exceptions.ImproperlyConfigured error
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_backend import routing
from .sio_app import sio
from socketio import ASGIApp

django_asgi_app = get_asgi_application()

application = ASGIApp(sio, django_asgi_app)

# Websockets / Channel implementation

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })

# # Attach Socket.IO app to ASGI app
# application = ASGIApp(sio, application)
