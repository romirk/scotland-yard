from cgitb import text
from uuid import uuid4
from django.test import TestCase

from .ws.GameConsumer import GameConsumer

from .engine.main import ScotlandYard
from .engine.constants import AVAILABLE_START_LOCATIONS
from channels.testing import WebsocketCommunicator

from .multiplayer import createRoom, getGameByID, getGameInfo, joinRoom, startRollCall


class EngineTestCase(TestCase):
    """
    Test game engine.
    """

    async def setUp(self) -> None:
        self.test_game_id = createRoom()
        self.game = getGameByID(self.test_game_id)

        self.player_ids = [uuid4() for _ in range(6)]

        for i in range(6):
            joinRoom(self.test_game_id, self.player_ids[i], f"player{i}")

        startRollCall(self.test_game_id)

        self.communicators = [WebsocketCommunicator(
            GameConsumer.as_asgi(), f"/game/{self.test_game_id}") for _ in range(6)]

        for communicator in self.communicators:
            connected, subprotocol = await communicator.connect()
            assert connected

        for i, player_id in enumerate(self.player_ids):
            await self.communicators[i].send_to(text_data=f"JOIN {player_id}")
            response = await communicator.receive_from()
            
        print("set up succesfully")
