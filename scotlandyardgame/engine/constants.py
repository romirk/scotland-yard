# constants for main.py
from __future__ import annotations
from enum import Enum, auto

from .mapdata import MAPDATA

SURFACE_MOVES = [1, 3, 8, 13, 18, 24]
CYCLE_LIMIT = 24
MAX_PLAYERS = 6

AVAILABLE_START_LOCATIONS = [
    13, 26, 29, 34, 50, 53  # , 91, 94, 103, 112, 117, 132, 138, 141, 155, 174, 197, 198
]
AVAILABLE_COLORS = [
    'red', 'blue', 'purple', 'green', 'yellow', 'orange'
]


class GameState(Enum):
    PENDING = "pending"
    CONNECTING = "connecting"
    RUNNING = "running"
    STOPPED = "stopped"


class EndState(Enum):
    NOT_ENDED = auto()
    DETECTIVES_WIN = auto()
    MR_X_WINS = auto()
    ABORTED = auto()

BLACK_TICKET, BUS_TICKET, TAXI_TICKET, UNDERGROUND_TICKET, DOUBLE_TICKET = 'black', 'bus', 'taxi', 'underground', 'double'
TICKET_TYPES = [TAXI_TICKET, BUS_TICKET, UNDERGROUND_TICKET, BLACK_TICKET]