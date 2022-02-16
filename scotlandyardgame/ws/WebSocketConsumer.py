from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from scotlandyardgame.ws.GameMessages import GameMessages
from scotlandyardgame.ws.LobbyMessages import LobbyMessages
from scotlandyardgame.ws.messages import Messages

from ..engine.constants import GameState
from ..multiplayer import get_game_by_id, leave_room, get_game_id_with_player
from scotlandyardgame import multiplayer

TRACK_DISCONNECTED = set()


class WebSocketConsumer(AsyncWebsocketConsumer):
    """
    Defines the handler for the websocket.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "generic"

    async def connect(self):
        self.game_id: str = self.scope["url_route"]["kwargs"]["game_id"]
        self.player_id: str = self.scope["url_route"]["kwargs"]["player_id"]
        self.message_service = GameMessages if self.type == "game" else LobbyMessages

        try:
            game = get_game_by_id(self.game_id)
        except ValueError as e:
            print(e)
            return

        print(f"ws-connecting: {self.channel_name} \033[33m{self.game_id}\033[0m")

        prev_state = game.state

        if game is not None:
            TRACK_DISCONNECTED.discard(self.player_id)

            if game.state == GameState.CONNECTING:
                multiplayer.answer_roll_call(self.game_id, self.player_id)
                
            print("\033[32maccepted\033[0m")
            await self.channel_layer.group_add(
                self.type + "_" + self.game_id, self.channel_name
            )
            await self.accept()

            await self.send(
                self.message_service.acknowledge(
                    game.id, TRACK_DISCONNECTED
                )
            )
            await self.group_send(self.message_service.player_joined(self.player_id))

            
            if prev_state != GameState.RUNNING and game.state == GameState.RUNNING:
                await self.group_send(GameMessages.game_starting())

    async def disconnect(self, close_code: int = 1006):
        print(f"disconnecting {self.player_id} with close code {close_code}")
        await self.channel_layer.group_discard(
            self.type + "_" + self.game_id, self.channel_name
        )

        TRACK_DISCONNECTED.add(self.player_id)
        game = get_game_by_id(self.game_id)
        state = game.state

        if close_code == 1000 and state != GameState.CONNECTING:
            await self.delayed_release(self.player_id, 0)
        else:
            await self.group_send(Messages.los(self.player_id))
            await self.delayed_release(self.player_id)

    async def ws_send(self, event):
        await self.send(event["text"])

    async def delayed_release(self, player_id: str, timeout: float = 3.0):
        if timeout > 0 and player_id in TRACK_DISCONNECTED:
            print(f"Now tracking {player_id} for {timeout} seconds")
            await sleep(timeout)

        if player_id not in TRACK_DISCONNECTED:
            return

        print(f"\033[33m{player_id}\033[0m is disconnected, releasing")
        TRACK_DISCONNECTED.remove(player_id)

        game = get_game_by_id(self.game_id)
        prev_host, prev_x = game.get_host_id(), game.get_mr_x()
        leave_room(self.game_id, player_id)

        if game.state == GameState.STOPPED:
            await self.group_send(Messages.abort())
            return
        new_host, new_x = game.get_host_id(), game.get_mr_x()

        await self.send_remove(
            player_id,
            new_host if new_host != prev_host else None,
            new_x if new_x != prev_x else None,
        )

    async def send_remove(self, player_id, new_host=None, new_x=None):
        await self.group_send(Messages.remove(player_id))
        if new_host is not None:
            await self.group_send(Messages.set_host(new_host))
        if new_x is not None:
            await self.group_send(Messages.set_mr_x(new_x))

    async def receive(self, text_data):
        print(
            f"\033[36m[ws/client\033[33m{' ' + self.player_id[:8]}\033[36m]\033[0m {text_data}"
        )
        await self.handler.process(text_data)

    def group_send(self, msg: str):
        return self.channel_layer.group_send(
            self.type + "_" + self.game_id, {"type": "ws.send", "text": msg}
        )
