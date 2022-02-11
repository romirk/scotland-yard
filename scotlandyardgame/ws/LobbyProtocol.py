from ..engine.constants import MAX_PLAYERS
from ..multiplayer import (
    get_game_host,
    get_game_id_with_player,
    get_player_ids,
    leave_room,
    set_color,
    set_mr_x,
    start_roll_call,
)
from .LobbyMessages import LobbyMessages
from .protocol import Protocol
from .WebSocketConsumer import TRACK_DISCONNECTED, WebSocketConsumer


class LobbyProtocol(Protocol):
    def __init__(self, consumer: WebSocketConsumer) -> None:
        super().__init__(
            consumer,
            {
                "REQCOLOR": self.reqcolor,
                "REQMRX": self.reqmrx,
                "LEAVE": self.leave,
                "READY": self.ready,
            },
        )
        self.player_id = None

    async def reqcolor(self, color: str):
        try:
            set_color(get_game_id_with_player(self.player_id), self.player_id, color)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.set_color(self.player_id, color))

    async def reqmrx(self, player_id):
        try:
            set_mr_x(get_game_id_with_player(self.player_id), self.player_id)
        except Exception as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.set_mr_x(player_id))

    async def leave(self):
        # leaveRoom(getGameIDWithPlayer(self.player_id), self.player_id)
        await self.group_send(LobbyMessages.remove(self.player_id))
        await self.consumer.close(code=1000, reason="Leaving")

    async def ready(self):
        print(f"{self.consumer.player_id} is ready")
        self.player_id = self.consumer.player_id
        if (
            get_game_host(game_id := get_game_id_with_player(self.player_id))
            != self.player_id
        ):
            print("Only host can start game")
            return
        c = 0
        for player in get_player_ids(game_id):
            if player in TRACK_DISCONNECTED:
                leave_room(game_id, player)
                TRACK_DISCONNECTED.remove(player)
            else:
                c += 1

        if c < MAX_PLAYERS:
            return
        try:
            start_roll_call(game_id)
        except RuntimeError as e:
            print(e)
        else:
            await self.group_send(LobbyMessages.start_game())
