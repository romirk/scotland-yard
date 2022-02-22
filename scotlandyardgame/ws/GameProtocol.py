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
                "MOVE": self.move,
                "GET_GAME_INFO": self.get_game_info,
                "GET_PLAYER_INFO": self.get_player_info,
                "HELP": self.help,
            },
        )

    async def move(self, ticket: str, *args):
        """request a move"""
        if self.consumer.game_id != multiplayer.get_game_id_with_player(
            self.consumer.player_id
        ):
            raise RuntimeError("Player is not in a game")
        if multiplayer.get_game_state(self.consumer.game_id) != GameState.RUNNING:
            raise RuntimeError("Game is not running")

        if ticket == DOUBLE_TICKET:
            move_data = multiplayer.move(
                self.consumer.game_id,
                self.consumer.player_id,
                DOUBLE_TICKET,
                {
                    "ticket1": args[0],
                    "location1": int(args[1]),
                    "ticket2": args[2],
                    "location2": int(args[3]),
                },
            )
        elif ticket == "pass":
            move_data = multiplayer.move(
                self.consumer.game_id, self.consumer.player_id, ticket, {}
            )
        else:
            move_data = multiplayer.move(
                self.consumer.game_id,
                self.consumer.player_id,
                ticket,
                {"location": int(args[0])},
            )

        if move_data["accepted"]:
            await self.group_send(GameMessages.player_moved(move_data))
            if move_data["game_state"] != GameState.RUNNING:
                await self.group_send(f"GAME_OVER {move_data['game_state']}")
                multiplayer.delete_game(self.consumer.game_id)

        else:
            await self.send(f"DENIED {move_data['message']}")

    async def get_game_info(self):
        """get information about the game"""
        await self.send(
            GameMessages.game_info(multiplayer.get_game_info(self.consumer.game_id))
        )

    async def get_player_info(self, player_id: str = None):
        """get information about yourself, or all players"""
        if player_id is None:
            player_id = self.consumer.player_id
        else:
            player_id = "ALL"

        await self.send(
            GameMessages.player_info(
                multiplayer.get_player_info(self.consumer.game_id, player_id)
            )
        )

    async def help(self):
        """display help and exit"""
        await self.send(GameMessages.help(self.handlers))
