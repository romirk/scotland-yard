from enum import Enum, auto
from player import Player

SURFACE_MOVES = [3, 8, 13, 18, 24]
MOVE_LIMIT = 24
MAX_PLAYERS = 6
TICKET_TYPES = ["taxi", "bus", "underground", "special"]


class GameState(Enum):
    PENDING = auto()
    CONNECTING = auto()
    RUNNING = auto()
    STOPPED = auto()


class ScotlandYard:
    """
    Instance of a ```ScotlandYard``` game. Stores all game information and handles game logic.
    """

    def __init__(self, gameID: str) -> None:
        self.ID: str = gameID
        self.state: GameState = GameState.PENDING
        self.players: dict[str, Player] = {}
        self.available_locations: list[int] = [
            34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50]
        self.available_colors: list[str] = ['red', 'blue',
                                 'purple', 'green', 'yellow', 'orange']
        self.moves: int = 0
        self.turn: int = 0

    def getPlayer(self, playerID: str) -> Player:
        """returns ```Player``` in current game with ID ```playerID```"""
        return self.players[playerID]

    def getPlayerAt(self, loc: int) -> Player:
        """returns ```Player``` in current game with location ```loc```"""
        for player in self.players.items():
            pass