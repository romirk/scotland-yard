from channels.generic.websocket import AsyncWebsocketConsumer

from .engine.constants import GameState
from .multiplayer import (getGameByID, getGameIDWithPlayer, leaveRoom,
                          setColor, setMrX, startGame)
from .protocols import LobbyProtocol


class SYConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        game = getGameByID(self.game_id)

        print(
            f"ws-connecting: {self.channel_name} \033[33m{self.game_id}\033[0m")

        if game is not None:
            print("accepted")
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.accept()
            await self.send("hello client")

    async def disconnect(self, close_code):
        print(f"disconnecting {self.channel_name} with close code {close_code}")
        if hasattr(self, 'player_id'):
            leaveRoom(self.game_id, self.player_id)
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.remove(self.player_id))
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def ws_send(self, event):
        await self.send(event["text"])


class LobbyRTConsumer(SYConsumer):

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') else ''}\033[36m]\033[0m {text_data}"
        )

        data = LobbyProtocol.parse(text_data)
        self.player_id = data.player_id

        if data.type == "JOIN":
            # JOIN player_id
            if getGameIDWithPlayer(self.player_id) != self.game_id:
                raise RuntimeError
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.newPlayer(self.player_id))
            await self.send(LobbyProtocol.acknowledge(self.game_id))

        elif data.type == "REQCOLOR":
            color = data.color
            try:
                setColor(self.game_id, self.player_id, color)
            except Exception as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.setColor(self.player_id))

        elif data.type == "REQMRX":
            try:
                setMrX(self.game_id, self.player_id)
            except Exception as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.setMrX(self.player_id))
        elif data.type == "READY":
            try:
                startGame(self.game_id)
            except RuntimeError as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.startGame())
        else:
            raise ValueError("invalid ws command")


class GameRTConsumer(SYConsumer):

    async def receive(self, text_data):
        print(f"[ws/client] {text_data}")
