from ..engine.constants import MAX_PLAYERS
from ..multiplayer import (getGameHost, getPlayerIDs, leaveRoom, setColor,
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
            "READY": self.ready
        })

    async def join(self, player_id: str):
        # JOIN player_id
        if player_id != self.__consumer.player_id:
            raise RuntimeError("player_id mismatch")
        await self.group_send(LobbyMessages.newPlayer(player_id))
        await self.send(LobbyMessages.acknowledge(self.game_id))
        if player_id in TRACK_DISCONNECTED:
            TRACK_DISCONNECTED.remove(player_id)
    
    async def reqcolor(self, player_id: str, color: str):
        try:
            setColor(self.game_id, player_id, color)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.setColor(player_id, color))
    
    async def reqmrx(self, player_id: str):
        try:
            setMrX(self.game_id, player_id)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.setMrX(player_id))
    
    async def disconnect(self, player_id: str):
        TRACK_DISCONNECTED.add(player_id)
        await self.__consumer.delayedRelease(0)
        await self.__consumer.channel_layer.group_discard(self.game_id, self.channel_name)
        await self.__consumer.close()

    async def ready(self):
        if getGameHost(self.game_id) != self.player_id:
            print("Only host can start game")
            return
        c = 0
        for player in getPlayerIDs(self.game_id):
            if player in TRACK_DISCONNECTED:
                leaveRoom(self.game_id, player)
                TRACK_DISCONNECTED.remove(player)
            else:
                c += 1

        if c < MAX_PLAYERS:
            return
        try:
            startRollCall(self.game_id)
        except RuntimeError as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.startGame())
