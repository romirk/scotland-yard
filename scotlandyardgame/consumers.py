import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .multiplayer import *

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
            await self.send("hello client")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def receive(self, text_data):
        print(f"[ws/client] {text_data}")

        
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