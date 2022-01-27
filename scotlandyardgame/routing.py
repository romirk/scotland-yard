from django.urls import re_path

from .ws.LobbyConsumer import LobbyConsumer
from .ws.GameConsumer import GameConsumer

websocket_urlpatterns = [
    re_path(r'^ws/lobby/(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            LobbyConsumer.as_asgi()),
    re_path(r'^ws/game/(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            GameConsumer.as_asgi())
]
