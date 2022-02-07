# constants for main.py
from __future__ import annotations
from enum import Enum, auto

SURFACE_MOVES = [2, 7, 12, 17, 23]
CYCLE_LIMIT = 24
MAX_PLAYERS = 6

AVAILABLE_START_LOCATIONS = [
    12,
    25,
    28,
    33,
    49,
    52,  # 90, 93, 102, 111, 116, 131, 137, 140, 154, 173, 196, 197
]
AVAILABLE_COLORS = ["red", "blue", "purple", "green", "yellow", "orange"]


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


BLACK_TICKET, BUS_TICKET, TAXI_TICKET, UNDERGROUND_TICKET, DOUBLE_TICKET = (
    "black",
    "bus",
    "taxi",
    "underground",
    "double",
)
TICKET_TYPES = [TAXI_TICKET, BUS_TICKET, UNDERGROUND_TICKET, BLACK_TICKET]
