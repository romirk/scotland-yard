from scotlandyardgame.ws.protocol import Protocol

from ..engine.constants import DOUBLE_TICKET, GameState
from ..multiplayer import (
    answerRollCall,
    deleteGame,
    getGameByID,
    getGameIDWithPlayer,
    getGameInfo,
    getGameState,
    getPlayerInfo,
    move,
)
from .GameMessages import GameMessages
from .protocol import Protocol
from .WebSocketConsumer import TRACK_DISCONNECTED, WebSocketConsumer


class GameProtocol(Protocol):
    def __init__(self, consumer: WebSocketConsumer) -> None:
        # TODO auto-detect handlers
        super().__init__(
            consumer,
            {
                "JOIN": self.join,
                "REQMOVE": self.reqmove,
                "GET_GAME_INFO": self.get_game_info,
                "GET_PLAYER_INFO": self.get_player_info,
            },
        )
        self.player_id = None
        self.game_id = None

    async def join(self, player_id: str):
        # JOIN player_id
        self.player_id = player_id
        if (game_id := getGameIDWithPlayer(player_id)) is None:
            raise RuntimeError("Player is not in a game")
        self.game_id = game_id

        if player_id not in getGameByID(self.game_id).rollCall:
            if getGameState(game_id) != GameState.CONNECTING:
                raise RuntimeError("Can't connect to this game")
            answerRollCall(game_id, player_id)
            await self.group_send(GameMessages.playerJoined(player_id))

        await self.send(GameMessages.acknowledge(game_id))

        if player_id in TRACK_DISCONNECTED:
            TRACK_DISCONNECTED.remove(player_id)

        if getGameState(game_id) == GameState.RUNNING:
            await self.group_send(GameMessages.gameStarting())

    async def reqmove(self, ticket: str, *args):
        if self.game_id != getGameIDWithPlayer(self.player_id):
            raise RuntimeError("Player is not in a game")
        if getGameState(self.game_id) != GameState.RUNNING:
            raise RuntimeError("Game is not running")

        if ticket == DOUBLE_TICKET:
            moveData = move(
                self.game_id,
                self.player_id,
                DOUBLE_TICKET,
                {
                    "ticket1": args[0],
                    "location1": int(args[1]),
                    "ticket2": args[2],
                    "location2": int(args[3]),
                },
            )
        elif ticket == "pass":
            moveData = move(self.game_id, self.player_id, ticket, {})
        else:
            moveData = move(
                self.game_id, self.player_id, ticket, {"location": int(args[0])}
            )

        if moveData["accepted"]:
            await self.group_send(GameMessages.playerMoved(moveData))
            if moveData["game_state"] != GameState.RUNNING:
                await self.group_send(f"GAME_OVER {moveData['game_state']}")
                deleteGame(self.game_id)

        else:
            await self.send(f"DENIED {moveData['message']}")

    async def get_game_info(self):
        await self.send(GameMessages.gameInfo(getGameInfo(self.game_id)))

    async def get_player_info(self, player_id: str = None):
        if player_id != "ALL":
            player_id = self.player_id
        await self.send(GameMessages.playerInfo(getPlayerInfo(self.game_id, player_id)))
