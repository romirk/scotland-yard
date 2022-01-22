from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer

from .engine.constants import MAX_PLAYERS, GameState
from .multiplayer import *
from .protocols import GameProtocol, LobbyProtocol

trackdisconnected = set()


class SYConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        try:
            game = getGameByID(self.game_id)
        except ValueError as e:
            print(e)
            return
        LobbyProtocol.trackdisconnected = trackdisconnected

        print(
            f"ws-connecting: {self.channel_name} \033[33m{self.game_id}\033[0m")

        if game is not None:
            print("accepted")
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        print(
            f"disconnecting {self.channel_name} with close code {close_code}")
        if hasattr(self, 'player_id'):
            # leaveRoom(self.game_id, self.player_id)
            game = getGameByID(self.game_id)
            if game is not None and game.state != GameState.CONNECTING:
                trackdisconnected.add(self.player_id)
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.LOS(self.player_id))
                await self.delayedRelease()
            else:
                await self.removeMessage()
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def ws_send(self, event):
        await self.send(event["text"])

    async def delayedRelease(self, timeout: float = 2.0):
        if timeout > 0:
            await sleep(timeout)
        if self.player_id in trackdisconnected:
            game = getGameByID(self.game_id)
            prevHost, prevX = game.getHostID(), game.getMrX()
            leaveRoom(self.game_id, self.player_id)
            if game.state == GameState.STOPPED:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.abort())
                return
            newHost, newX = game.getHostID(), game.getMrX()
            await self.removeMessage(
                newHost if newHost != prevHost else None,
                newX if newX != prevX else None
            )

    async def removeMessage(self, newHost=None, newX=None):
        await self.channel_layer.group_send(self.game_id, LobbyProtocol.remove(self.player_id))
        if newHost is not None:
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.setHost(newHost))
        if newX is not None:
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.setMrX(newX))


class LobbyRTConsumer(SYConsumer):

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') else ''}\033[36m]\033[0m {text_data}"
        )

        data = LobbyProtocol.parse(text_data)
        self.player_id = data.player_id if not hasattr(
            self, 'player_id') else self.player_id

        if data.type == "JOIN":
            # JOIN player_id
            if getGameIDWithPlayer(self.player_id) != self.game_id:
                raise RuntimeError
            await self.channel_layer.group_send(self.game_id, LobbyProtocol.newPlayer(self.player_id))
            await self.send(LobbyProtocol.acknowledge(self.game_id))
            if self.player_id in trackdisconnected:
                trackdisconnected.remove(self.player_id)

        elif data.type == "REQCOLOR":
            color = data.color
            try:
                setColor(self.game_id, self.player_id, color)
            except Exception as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.setColor(self.player_id, color))

        elif data.type == "REQMRX":
            try:
                setMrX(self.game_id, data.target)
            except Exception as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.setMrX(data.target))
        elif data.type == "DISCONNECT":
            trackdisconnected.add(self.player_id)
            await self.delayedRelease(0)
            await self.channel_layer.group_discard(self.game_id, self.channel_name)
            await self.close()
        elif data.type == "READY":
            if getGameHost(self.game_id) != self.player_id:
                print("Only host can start game")
                return
            c = 0
            for player in getPlayerIDs(self.game_id):
                if player in trackdisconnected:
                    leaveRoom(self.game_id, player)
                    trackdisconnected.remove(player)
                else:
                    c += 1

            if c < MAX_PLAYERS:
                return
            try:
                startRollCall(self.game_id)
            except RuntimeError as e:
                print(e)
            else:
                await self.channel_layer.group_send(self.game_id, LobbyProtocol.startGame())
        else:
            raise ValueError("invalid ws command")


class GameRTConsumer(SYConsumer):

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8] if hasattr(self, 'player_id') else ''}\033[36m]\033[0m {text_data}"
        )

        data = GameProtocol.parse(text_data)
        if data is None:
            print("invalid ws command (probably)")
            return
        self.player_id = data.player_id if not hasattr(self, 'player_id') else self.player_id


        if data.type == "JOIN":
            if getGameIDWithPlayer(self.player_id) != self.game_id:
                raise RuntimeError
            if getGameState(self.game_id) != GameState.CONNECTING:
                raise RuntimeError("Can't connect to this game")

            answerRollCall(self.game_id, self.player_id)
            
            await self.channel_layer.group_send(self.game_id, GameProtocol.playerJoined(self.player_id))
            await self.send(GameProtocol.acknowledge(self.game_id))
            if self.player_id in trackdisconnected:
                trackdisconnected.remove(self.player_id)

            if getGameState(self.game_id) == GameState.RUNNING:
                await self.channel_layer.group_send(self.game_id, GameProtocol.gameStarting())

        elif data.type == "REQMOVE":
            try:
                moveMade = move(self.game_id, self.player_id, data.ticket, data.movedata)
                await self.channel_layer.group_send(self.game_id, GameProtocol.playerMoved(moveMade))
                if moveMade["is_mr_x"]:
                    await self.send(GameProtocol.updateMrX(moveMade["destination"]))
            except:
                raise NotImplementedError
        
        elif data.type == "GET_GAME_INFO":
            await self.send(GameProtocol.gameInfo(getGameInfo(self.game_id)))