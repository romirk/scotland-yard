from django.test import TestCase

from .engine.main import ScotlandYard
from .engine.constants import AVAILABLE_START_LOCATIONS

class EngineTestCase(TestCase):
    """
    Test game engine.
    """

    def setUp(self) -> None:
        self.test_game_id = "12345678-1234-1234-1234-123456789012"
        self.game = ScotlandYard(self.test_game_id)
        self.game.addPlayer("A", "Player A")
        self.game.addPlayer("B", "Player B")
        self.game.addPlayer("C", "Player C")
        self.game.addPlayer("D", "Player D")
        self.game.addPlayer("E", "Player E")
        self.game.addPlayer("F", "Player F")
        self.game.rollCall.add(e for e in "ABCDEF")

        self.game.start()

    
