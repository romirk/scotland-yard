import json
from os import name
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

        message = text_data.split()
        type = message[0]
        
        if type == "JOIN":
            # JOIN player_id
            player_id = message[1]
            if getGameIDWithPlayer(player_id) != self.game_id:
                raise RuntimeError
            playerInfo = getPlayerInfo(player_id)
            await self.channel_layer.group_send(f"NEW_PLAYER {player_id} {playerInfo['name']} {playerInfo['color']} {playerInfo['is_mr_x']}")
            connected_players = [getPlayerInfo(p) for p in getPlayerIDs(self.game_id)]
            self.send(f"ACKNOWLEDGE {len(connected_players)}" +\
                "\n".join(f"{p_info['player_id']} {p_info['name']} {p_info['color']} {p_info['is_mr_x']}" for p_info in connected_players))
        
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