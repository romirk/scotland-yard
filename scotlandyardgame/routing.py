from django.urls import re_path

from .ws.GameConsumer import GameConsumer
from .ws.LobbyConsumer import LobbyConsumer

UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

websocket_urlpatterns = [
    re_path(
        r"^ws/lobby/(?P<game_id>" + UUID_RE + r")/(?P<player_id>" + UUID_RE + ")$",
        LobbyConsumer.as_asgi(),
    ),
    re_path(
        r"^ws/game/(?P<game_id>" + UUID_RE + r")/(?P<player_id>" + UUID_RE + ")$",
        GameConsumer.as_asgi(),
    ),
]
