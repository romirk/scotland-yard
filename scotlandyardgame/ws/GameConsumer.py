from .WebSocketConsumer import WebSocketConsumer
from .GameProtocol import GameProtocol


class GameConsumer(WebSocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = GameProtocol(self)
        self.player_id = None
