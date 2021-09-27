# constants for main.py

from enum import Enum, auto

from .mapdata import MAPDATA

SURFACE_MOVES = [3, 8, 13, 18, 24]
CYCLE_LIMIT = 24
MAX_PLAYERS = 6
TICKET_TYPES = ["taxi", "bus", "underground", "special"]

AVAILABLE_MOVES = [
    13, 26, 29, 34, 50, 53, 91, 94, 103, 112, 117, 132, 138, 141, 155, 174, 197, 198
]
AVAILABLE_COLORS = [
    'red', 'blue', 'purple', 'green', 'yellow', 'orange'
]


class GameState(Enum):
    PENDING = auto()
    CONNECTING = auto()
    RUNNING = auto()
    STOPPED = auto()

class EndState(Enum):
    NOT_ENDED = auto()
    DETECTIVES_WIN = auto()
    MR_X_WINS = auto()
    ABORTED = auto()
    