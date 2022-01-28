from ..engine.constants import MAX_PLAYERS
from ..multiplayer import (getGameHost, getGameIDWithPlayer, getPlayerIDs, leaveRoom, setColor,
                           setMrX, startRollCall)
from .LobbyMessages import LobbyMessages
from .protocol import Protocol
from .WebSocketConsumer import TRACK_DISCONNECTED, WebSocketConsumer


class LobbyProtocol(Protocol):
    def __init__(self, consumer: WebSocketConsumer) -> None:
        super().__init__(consumer, {
            "JOIN": self.join,
            "REQCOLOR": self.reqcolor,
            "REQMRX": self.reqmrx,
            "DISCONNECT": self.disconnect,
            "LEAVE": self.leave,
            "READY": self.ready
        })

    async def join(self, player_id: str):
        # JOIN player_id
        await self.group_send(LobbyMessages.newPlayer(player_id))
        await self.send(LobbyMessages.acknowledge(getGameIDWithPlayer(player_id)))
        if player_id in TRACK_DISCONNECTED:
            TRACK_DISCONNECTED.remove(player_id)
        self.consumer.player_id = player_id

    async def reqcolor(self, color: str):
        try:
            setColor(getGameIDWithPlayer(self.consumer.player_id),
                     self.consumer.player_id, color)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.setColor(self.consumer.player_id, color))

    async def reqmrx(self):
        try:
            setMrX(getGameIDWithPlayer(self.consumer.player_id),
                   self.consumer.player_id)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.setMrX(self.consumer.player_id))

    async def disconnect(self):
        TRACK_DISCONNECTED.add(self.consumer.player_id)
        await self.consumer.delayedRelease(self.consumer.player_id, 0)
        await self.consumer.channel_layer.group_discard(self.consumer.game_id, self.consumer.channel_name)
        await self.consumer.close()

    async def leave(self):
        leaveRoom(getGameIDWithPlayer(self.consumer.player_id),
                  self.consumer.player_id)
        await self.group_send(LobbyMessages.remove(self.consumer.player_id))

    async def ready(self):
        if getGameHost(game_id := getGameIDWithPlayer(self.consumer.player_id)) != self.consumer.player_id:
            print("Only host can start game")
            return
        c = 0
        for player in getPlayerIDs(game_id):
            if player in TRACK_DISCONNECTED:
                leaveRoom(self.game_id, player)
                TRACK_DISCONNECTED.remove(player)
            else:
                c += 1

        if c < MAX_PLAYERS:
            return
        try:
            startRollCall(game_id)
        except RuntimeError as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.startGame())
