from channels.generic.websocket import AsyncWebsocketConsumer

from .multiplayer import (getGameByID, getGameIDWithPlayer)
from .protocols import LobbyProtocol

mapPlayerToConn: dict[str, AsyncWebsocketConsumer] = dict()


class LobbyRTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        game = getGameByID(self.game_id)

        print(f"ws-connecting: {self.channel_name} {self.game_id}")

        if game is not None:
            print("accepted")
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.accept()
            # await self.send("hello client")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def receive(self, text_data):
        print(f"[ws/client] {text_data}")

        data = LobbyProtocol.parse(text_data)

        if data.type == "JOIN":
            # JOIN player_id
            player_id = data.player_id
            if getGameIDWithPlayer(player_id) != self.game_id:
                raise RuntimeError
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.newPlayer(self.game_id, player_id))
            await self.send(LobbyProtocol.acknowledge(self.game_id))

        else:
            raise ValueError


class GameRTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        game = getGameByID(self.game_id)

        print(f"ws-connecting: {self.channel_name} {self.game_id}")

        if game is not None:
            print("accepted")
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.accept()
            await self.send("hello client")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def receive(self, text_data):
        print(f"[ws/client] {text_data}")
