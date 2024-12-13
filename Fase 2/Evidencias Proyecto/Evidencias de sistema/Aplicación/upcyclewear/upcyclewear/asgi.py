# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from aplicacion.routing import websocket_urlpatterns  # Asegúrate de que este archivo exista

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upcyclewear.settings')  # Cambia 'myproject' por tu nombre de proyecto

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
