from .WebSocketConsumer import WebSocketConsumer
from .LobbyProtocol import LobbyProtocol


class LobbyConsumer(WebSocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = LobbyProtocol(self)
