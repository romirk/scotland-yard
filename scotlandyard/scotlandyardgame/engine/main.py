from enum import Enum, auto
from player import Player
from map import Map

SURFACE_MOVES = [3, 8, 13, 18, 24]
MOVE_LIMIT = 24
MAX_PLAYERS = 6
TICKET_TYPES = ["taxi", "bus", "underground", "special"]

MAP = Map([])


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
        # private
        self.__ID: str = gameID
        self.__available_locations: list[int] = [
            34, 174, 132, 26, 198, 141, 94, 29, 53, 13, 112, 103, 155, 138, 117, 91, 197, 50]
        self.__available_colors: list[str] = ['red', 'blue',
                                              'purple', 'green', 'yellow', 'orange']
        self.__moves: int = 0
        self.__turn: int = 0
        self.__mrX: Player = None

        # public
        self.state: GameState = GameState.PENDING
        self.players: dict[str, Player] = {}

    # getters

    @property
    def ID(self) -> str:
        return self.__ID

    # setters

    @ID.setter
    def ID(self, newID: str):
        raise AttributeError("ID assignment not allowed.")

    # methods

    def getPlayerByID(self, playerID: str) -> Player:
        """returns ```Player``` in current game with ID ```playerID```"""
        return self.players[playerID]

    def getPlayerAt(self, loc: int) -> Player:
        """returns ```Player``` in current game with location ```loc```"""
        for player in self.players.items():
            if player.location == loc:
                return player
    
    def getPlayerIDs(self) -> list[str]:
        """Get a list of connected player IDs"""
        return [p.ID for p in self.players]

    def getPlayerNames(self) -> list[str]:
        """Get a list of connected player names"""
        return [p.name for p in self.players]

    def isValidMove(self, player_id, location, ticket) -> bool:
        """checks if player with ```player_id``` can move to ```location``` using ```ticket```"""
        player = self.getPlayerByID(player_id)
        return player is not None \
            and (ticket != "special" or player.is_mr_x) \
            and player.getTickets(ticket) > 0 \
            and location in MAP.stations[player.location].getNeighbours(ticket) \
            and (self.getPlayerAt(location) is None or (not player.is_mr_x and self.getPlayerAt(location) == self.__mrX))

    def advanceTurn(self):
        self.__turn = (self.__turn + 1) % 6
        if not self.__turn:
            self.__moves += 1
