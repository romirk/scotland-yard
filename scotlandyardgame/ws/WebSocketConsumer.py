from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from scotlandyardgame.ws.messages import Messages


from ..engine.constants import GameState
from ..multiplayer import *

TRACK_DISCONNECTED = set()


class WebSocketConsumer(AsyncWebsocketConsumer):
    """
    Defines the handler for the websocket.
    """

    async def connect(self):
        self.game_id: str = self.scope["url_route"]["kwargs"]["game_id"]
        self.scope["game_data"] = {"game_id": self.game_id}
        try:
            game = getGameByID(self.game_id)
        except ValueError as e:
            print(e)
            return

        print(f"ws-connecting: {self.channel_name} \033[33m{self.game_id}\033[0m")

        if game is not None:
            print("accepted")
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        print(f"disconnecting {self.channel_name} with close code {close_code}")
        await self.channel_layer.group_discard(self.game_id, self.channel_name)
        if hasattr(self, 'player_id'):
            # leaveRoom(self.game_id, self.player_id)
            game = getGameByID(self.game_id)
            if game is not None and game.state != GameState.CONNECTING:
                TRACK_DISCONNECTED.add(self.player_id)
                await self.group_send(Messages.LOS(self.player_id))
                await self.delayedRelease(self.player_id)
            else:
                await self.removeMessage()

    async def ws_send(self, event):
        await self.send(event["text"])

    async def delayedRelease(self, player_id: str, timeout: float = 2.0):
        if timeout > 0 and player_id in TRACK_DISCONNECTED:
            await sleep(timeout)
        game = getGameByID(self.game_id)
        prevHost, prevX = game.getHostID(), game.getMrX()
        leaveRoom(self.game_id, player_id)
        if game.state == GameState.STOPPED:
            await self.group_send(Messages.abort())
            return
        newHost, newX = game.getHostID(), game.getMrX()

        await self.removeMessage(
            player_id,
            newHost if newHost != prevHost else None,
            newX if newX != prevX else None
        )


    async def removeMessage(self,player_id, newHost=None, newX=None):
        await self.group_send(Messages.remove(player_id))
        if newHost is not None:
            await self.group_send(Messages.setHost(newHost))
        if newX is not None:
            await self.group_send(Messages.setMrX(newX))

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') and self.player_id is not None else ''}\033[36m]\033[0m {text_data}"
        )
        self.player_id = text_data.split()[1] if len(text_data.split()) > 1 else None
        await self.handler.process(text_data)
        self.player_id = self.handler.player_id

    def group_send(self, msg: str):
        return self.channel_layer.group_send(
            self.game_id, {"type": "ws.send", "text": msg}
        )
