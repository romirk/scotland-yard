from scotlandyardgame.ws.protocol import Protocol

from ..engine.constants import GameState
from ..multiplayer import (answerRollCall, getGameIDWithPlayer, getGameInfo,
                           getGameState)
from .GameMessages import GameMessages
from .protocol import Protocol
from .WebSocketConsumer import TRACK_DISCONNECTED, WebSocketConsumer


class GameProtocol(Protocol):
    def __init__(self, consumer: WebSocketConsumer, fmap: dict[str, function]) -> None:
        super().__init__(consumer, {
            "JOIN": self.join,
            "REQMOVE": self.reqmove,
            "GET_GAME_INFO": self.get_game_info
        })

    async def join(self, player_id: str):
        # JOIN player_id
        if getGameIDWithPlayer(player_id) != self.game_id:
            raise RuntimeError
        if getGameState(self.game_id) != GameState.CONNECTING:
            raise RuntimeError("Can't connect to this game")

        answerRollCall(self.game_id, player_id)

        await self.group_send(GameMessages.playerJoined(player_id))
        await self.send(GameMessages.acknowledge(self.game_id))
        if player_id in TRACK_DISCONNECTED:
            TRACK_DISCONNECTED.remove(self.player_id)

        if getGameState(self.game_id) == GameState.RUNNING:
            await self.group_send(GameMessages.gameStarting())

    async def reqmove(self, player_id: str, ticket: str, *args):
        # TODO implement
        pass

    async def get_game_info(self):
        await self.send(GameMessages.gameInfo(getGameInfo(self.game_id)))
