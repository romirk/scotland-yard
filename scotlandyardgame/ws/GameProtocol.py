from scotlandyardgame.ws.protocol import Protocol

from .. import multiplayer
from ..engine.constants import DOUBLE_TICKET, GameState
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
        if (game_id := multiplayer.get_game_id_with_player(player_id)) is None:
            raise RuntimeError("Player is not in a game")
        self.game_id = game_id

        if player_id not in multiplayer.get_game_by_id(self.game_id).rollCall:
            if multiplayer.get_game_state(game_id) != GameState.CONNECTING:
                raise RuntimeError("Can't connect to this game")
            multiplayer.answer_roll_call(game_id, player_id)
            await self.group_send(GameMessages.player_joined(player_id))

        if multiplayer.get_game_state(game_id) == GameState.RUNNING:
            await self.group_send(GameMessages.game_starting())

    async def reqmove(self, ticket: str, *args):
        if self.game_id != multiplayer.get_game_id_with_player(self.player_id):
            raise RuntimeError("Player is not in a game")
        if multiplayer.get_game_state(self.game_id) != GameState.RUNNING:
            raise RuntimeError("Game is not running")

        if ticket == DOUBLE_TICKET:
            move_data = multiplayer.move(
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
            move_data = multiplayer.move(self.game_id, self.player_id, ticket, {})
        else:
            move_data = multiplayer.move(
                self.game_id, self.player_id, ticket, {"location": int(args[0])}
            )

        if move_data["accepted"]:
            await self.group_send(GameMessages.player_moved(move_data))
            if move_data["game_state"] != GameState.RUNNING:
                await self.group_send(f"GAME_OVER {move_data['game_state']}")
                multiplayer.delete_game(self.game_id)

        else:
            await self.send(f"DENIED {move_data['message']}")

    async def get_game_info(self):
        await self.send(GameMessages.game_info(multiplayer.get_game_info(self.game_id)))

    async def get_player_info(self, player_id: str = None):
        if player_id != "ALL":
            player_id = self.player_id
        await self.send(
            GameMessages.player_info(
                multiplayer.get_player_info(self.game_id, player_id)
            )
        )
