import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Import your routing file
from a_rtchat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

# Create the default Django ASGI application
django_asgi_app = get_asgi_application()

from a_rtchat import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Handle HTTP requests with Django's ASGI app
    "websocket": AllowedHostsOriginValidator(  # WebSocket handling with allowed hosts validation
        AuthMiddlewareStack(  # WebSocket authentication middleware
            URLRouter(routing.websocket_urlpatterns))  # Define your WebSocket routing
        ),
})
