from django.test import SimpleTestCase

from .engine.main import ScotlandYard


class SYTestCase(SimpleTestCase):
    def test_game(self):
        game_id = "12345678-1234-1234-1234-123456789012"
        game = ScotlandYard(game_id)

        # tests
        self.assertEqual(game_id, game.ID)
        with self.assertRaises(AttributeError):
            game.ID = "can't set this"
        
        