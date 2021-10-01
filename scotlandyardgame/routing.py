from django.urls import re_path

from .consumers import GameRTConsumer

websocket_urlpatterns = [
    re_path( r'^ws/(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', GameRTConsumer.as_asgi())
]
