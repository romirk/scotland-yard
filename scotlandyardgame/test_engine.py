from uuid import uuid4

from channels.testing import WebsocketCommunicator
from django.test import TestCase

from .multiplayer import create_room, get_game_by_id, join_room, start_roll_call
from .ws.GameConsumer import GameConsumer

### TODO uhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh


class EngineTestCase(TestCase):
    """
    Test game engine.
    """

    def setUp(self) -> None:
        self.test_game_id = create_room()
        self.game = get_game_by_id(self.test_game_id)

        self.player_ids = [uuid4() for _ in range(6)]

        for i in range(6):
            join_room(self.test_game_id, self.player_ids[i], f"player{i}")

        start_roll_call(self.test_game_id)

        self.communicators = [
            WebsocketCommunicator(GameConsumer.as_asgi(), f"/game/{self.test_game_id}")
            for _ in range(6)
        ]

        print("\033[32mset up succesfully\033[0m")

    async def start_comms(self):
        for communicator in self.communicators:
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected)
        print("connected")

        for i, player_id in enumerate(self.player_ids):
            await self.communicators[i].send_to(text_data=f"JOIN {player_id}")
            response = await communicator.receive_from()

    async def do_roll_call(self):
        await self.start_comms()
        # do stuff

    async def test_basic(self):
        # await self.start_comms()
        pass
