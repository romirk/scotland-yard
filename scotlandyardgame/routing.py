from django.urls import re_path

from .consumers import GameRTConsumer, LobbyRTConsumer

websocket_urlpatterns = [
    re_path(r'^ws/lobby/(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            LobbyRTConsumer.as_asgi()),
    re_path(r'^ws/game/(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$',
            GameRTConsumer.as_asgi())
]
