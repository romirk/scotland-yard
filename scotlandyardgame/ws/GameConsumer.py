from .WebSocketConsumer import WebSocketConsumer
from .GameProtocol import GameProtocol


class GameConsumer(WebSocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = GameProtocol(self)

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') else ''}\033[36m]\033[0m {text_data}"
        )
