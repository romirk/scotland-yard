from flask import request
from scotlandyardgame.ws.protocol import Protocol

from ..engine.constants import GameState, Ticket
from ..multiplayer import (answerRollCall, getGameIDWithPlayer, getGameInfo,
                           getGameState, move)
from .GameMessages import GameMessages
from .protocol import Protocol
from .WebSocketConsumer import TRACK_DISCONNECTED, WebSocketConsumer


class GameProtocol(Protocol):
    def __init__(self, consumer: WebSocketConsumer) -> None:
        super().__init__(consumer, {
            "JOIN": self.join,
            "REQMOVE": self.reqmove,
            "GET_GAME_INFO": self.get_game_info
        })

    async def join(self, player_id: str):
        # JOIN player_id
        if getGameIDWithPlayer(player_id) != self.game_id:
            raise RuntimeError("Player is not in a game")
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
        if getGameIDWithPlayer(player_id) != self.game_id:
            raise RuntimeError("Player is not in a game")
        if getGameState(self.game_id) != GameState.RUNNING:
            raise RuntimeError("Game is not running")

        moveData = (move(self.game_id, player_id, Ticket.DOUBLE, {"ticket1": args[0], "location1": args[1], "ticket2": args[2], "location2": args[3]})
                    if ticket == Ticket.DOUBLE else
                    move(self.game_id, player_id,
                         ticket, {"location": args[0]})
                    )

        await self.group_send(GameMessages.playerMoved(player_id, moveData))

    async def get_game_info(self):
        await self.send(GameMessages.gameInfo(getGameInfo(self.game_id)))
