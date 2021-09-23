from enum import Enum, auto
from random import randrange

from .map import Map
from .mapdata import MAPDATA
from .player import Player

SURFACE_MOVES = [3, 8, 13, 18, 24]
MOVE_LIMIT = 24
MAX_PLAYERS = 6
TICKET_TYPES = ["taxi", "bus", "underground", "special"]

MAP = Map(MAPDATA)


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

    # private methods

    def __getPlayerByID(self, playerID: str) -> Player:
        """returns ```Player``` in current game with ID ```playerID```"""
        return self.players[playerID]

    def __getPlayerAt(self, loc: int) -> Player:
        """returns ```Player``` in current game with location ```loc```"""
        for player in self.players.items():
            if player.location == loc:
                return player

    def __isValidMove(self, player_id: str, location: int, ticket: str) -> bool:
        """checks if player with ```player_id``` can move to ```location``` using ```ticket```"""
        player = self.__getPlayerByID(player_id)
        return player is not None \
            and (ticket != "special" or player.is_mr_x) \
            and player.getTickets(ticket) > 0 \
            and location in MAP.stations[player.location].getNeighbours(ticket) \
            and (self.__getPlayerAt(location) is None or (not player.is_mr_x and self.getPlayerAt(location) == self.__mrX))

    def __advanceTurn(self):
        self.__turn = (self.__turn + 1) % 6
        if not self.__turn:
            self.__moves += 1

    # public methods

    def getPlayerIDs(self) -> list[str]:
        """Get a list of connected player IDs"""
        return [p.ID for p in self.players]

    def getPlayerNames(self) -> list[str]:
        """Get a list of connected player names"""
        return [p.name for p in self.players]

    def getPlayerInfo(self, player_id: str) -> dict:
        p = self.__getPlayerByID(player_id)
        return {
            "game_id": self.__ID,
            "player_id": player_id,
            "name": p.name, 
            "color": p.color, 
            "location": p.location, 
            "is_mr_x": p.is_mr_x
            }

    def setMrX(self, player_id: str):
        player = self.__getPlayerByID(player_id)
        oldX = self.__mrX
        oldX.is_mr_x = False
        player.is_mr_x = True
        self.__mrX = player
        oldX.color = player.color
        player.color = 'X'

    def addPlayer(self, player_id: str, player_name: str):
        # raise NotImplementedError()
        print(f"\tregistering {player_name}...")
        if len(self.players) >= MAX_PLAYERS:
            raise RuntimeError("Game is full!")
        if player_id in self.players:
            raise ValueError("player already connected")

        is_mr_x = not self.players  # true when self.players is empty
        print(f"\t\tMr. X: {is_mr_x}")

        if is_mr_x:
            col = 'X'
        else:
            col_index = randrange(len(self.__available_colors))
            col = self.__available_colors[col_index]
            del self.__available_colors[col_index]

        print(f"\t\tcolor: {col}")

        loc_index = randrange(len(self.__available_locations))
        loc = self.__available_locations[loc_index]
        del self.__available_locations[loc_index]

        print(f"\t\tlocation: {loc}")

        newPlayer = Player(player_id, player_name, loc, col, is_mr_x)
        self.players[player_id] = newPlayer

        print("\tdone.\ntotal players connected: " + str(len(self.players)))

        self.players[player_id] = newPlayer
