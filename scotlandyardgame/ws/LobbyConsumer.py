from .WebSocketConsumer import WebSocketConsumer, TRACK_DISCONNECTED
from .LobbyProtocol import LobbyProtocol

class LobbyConsumer(WebSocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = LobbyProtocol(self)

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') else ''}\033[36m]\033[0m {text_data}"
        )

        await self.handler.process(text_data)

