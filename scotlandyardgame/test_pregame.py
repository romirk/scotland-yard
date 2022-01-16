from django.test import TestCase

from .engine.main import ScotlandYard
from .engine.constants import AVAILABLE_START_LOCATIONS


class PreGameTestCase(TestCase):
    """
    Basic tests before game starts.
    """

    def setUp(self):
        self.test_game_id = "12345678-1234-1234-1234-123456789012"
        self.game = ScotlandYard(self.test_game_id)
        self.game.addPlayer("A", "Player A")

    def test_game_id(self):
        '''
        Testing whether game ID is correct and immutable
        '''
        self.assertEqual(self.test_game_id, self.game.ID)
        with self.assertRaises(AttributeError):
            self.game.ID = "can't set this"

    def test_player(self):
        self.assertEqual(len(self.game.getPlayerIDs()), 1)
        self.assertEqual(self.game.getPlayerIDs()[0], "A")
        self.assertEqual(self.game.getHostID(), "A")
        info = self.game.getPlayerInfo("A")
        self.assertEqual(info["color"], "X")
        self.assertIn(info["location"], AVAILABLE_START_LOCATIONS)

    def test_add_same_player(self):
        '''
        Adding another player with the same id
        '''
        with self.assertRaises(ValueError):
            self.game.addPlayer("A", "Also A")

    def test_add_player(self):
        '''
        Adding a new player 
        '''
        self.game.addPlayer("B", "Player B")
        player_IDs = self.game.getPlayerIDs()
        self.assertEqual(len(player_IDs), 2)
        self.assertIn("B", player_IDs)
        self.assertEqual(self.game.getHostID(), "A")
        infoA = self.game.getPlayerInfo("A")
        infoB = self.game.getPlayerInfo("B")
        self.assertNotEqual(infoA["location"], infoB["location"])
        self.assertNotEqual(infoA["color"], infoB["color"])

    def test_start_game_1_player(self):
        with self.assertRaises(RuntimeError, msg="Invalid number of players: 1"):
            self.game.start()

    def test_add_excess_players(self):
        for i in range(66, 66+5):
            self.game.addPlayer(chr(i), f"Player {chr(i)}")
        player_IDs = self.game.getPlayerIDs()
        self.assertEqual(len(player_IDs), 6)

        with self.assertRaises(RuntimeError, msg="Game is full!"):
            self.game.addPlayer("G", "Unwanted")

    def test_change_color_nonexistent_color(self):
        with self.assertRaises(ValueError):
            self.game.setColor("A", "Blurple")

    def test_change_color_mr_x(self):
        with self.assertRaises(RuntimeError):
            self.game.setColor("A", "green")

    def test_change_color_to_x(self):
        self.game.addPlayer("B", "Player B")
        with self.assertRaises(ValueError):
            self.game.setColor("B", "X")

    def test_change_color(self):
        self.game.addPlayer("B", "Player B")
        colorB = self.game.getPlayerInfo("B")["color"]
        isGreen = colorB == "green"
        self.game.setColor("B", "green" if not isGreen else "blue")
        colorB = self.game.getPlayerInfo("B")["color"]
        self.assertEqual(colorB, "green" if not isGreen else "blue")

    def test_change_to_same_color(self):
        self.game.addPlayer("B", "Player B")
        self.game.setColor("B", "green")
        self.game.setColor("B", "green")
        colorB = self.game.getPlayerInfo("B")["color"]
        self.assertEqual(colorB, "green")

    def test_nonexistent_player(self):
        with self.assertRaises(ValueError):
            self.game.getPlayerInfo("C")

    def test_remove_player(self):
        self.game.addPlayer("B", "Player B")
        self.game.removePlayer("B")
        self.assertEqual(len(self.game.getPlayerIDs()), 1)
    
    def test_remove_host(self):
        self.game.addPlayer("B", "Player B")
        print(self.game.getPlayerIDs())
        print(self.game.getPlayerInfo("A"))
        self.game.removePlayer("A")
        self.assertEqual(self.game.getHostID(), "B")
        self.assertEqual(self.game.getMrX(), "B")

    def test_set_mr_x(self):
        self.game.addPlayer("B", "Player B")
        self.game.setMrX("B")
        self.assertEqual(self.game.getMrX(), "B")

    def test_set_mr_x_nonexistent_player(self):
        with self.assertRaises(ValueError):
            self.game.setMrX("C")

    def test_set_mr_x_already_mr_x(self):
        self.game.setMrX("A")
        self.assertEqual(self.game.getMrX(), "A")

    