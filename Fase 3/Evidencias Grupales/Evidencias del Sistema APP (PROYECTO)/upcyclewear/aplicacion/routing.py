# chat/routing.py

from django.urls import re_path
from . import consumers  # Asegúrate de que tienes un consumer definido

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversacion_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
