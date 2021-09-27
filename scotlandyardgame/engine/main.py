from random import choice, randrange
from typing import Final

from .constants import *
from .map import Map
from .player import Player

MAP = Map(MAPDATA)


class ScotlandYard:
    """
    Instance of a ```ScotlandYard``` game. Stores all game information and handles game logic.

    """

    def __init__(self, gameID: str) -> None:
        # private
        self.__ID: Final = gameID
        self.__players: dict[str, Player] = {}

        self.__available_locations: list[int] = AVAILABLE_MOVES.copy()
        self.__available_colors: list[str] = AVAILABLE_COLORS.copy()

        # cycle = everyone gets 1 move
        self.__moves: int = 0
        self.__cycle: int = 0
        self.__mrX: Player = None

        # public
        self.state: GameState = GameState.PENDING

    # getters

    @property
    def ID(self) -> str:
        return self.__ID

    # setters

    @ID.setter
    def ID(self, *args):
        raise AttributeError("ID assignment not allowed.")

    # private methods

    def __getPlayerByID(self, playerID: str) -> Player:
        """returns ```Player``` in current game with ID ```playerID```"""
        if playerID not in self.__players:
            raise ValueError("player does not exist in this game")
        return self.__players[playerID]

    def __getPlayerAt(self, loc: int) -> Player:
        """returns ```Player``` in current game with location ```loc```"""
        for player in self.__players.items():
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

    def __getWhoseTurn(self) -> Player:
        # TODO get whose turn
        if not self.__moves:
            return self.__mrX

    def __advanceTurn(self):
        self.__cycle = (self.__cycle + 1) % 6
        if not self.__cycle:
            self.__moves += 1

    # public methods

    def getPlayerIDs(self) -> list[str]:
        """Get a list of connected player IDs"""
        return [p.ID for p in self.__players]

    def getPlayerNames(self) -> list[str]:
        """Get a list of connected player names"""
        return [p.name for p in self.__players]

    def getPlayerInfo(self, player_id: str) -> dict:
        """
        returns a ```dict``` containing information about a specified player

        {
            "game_id",
            "player_id",
            "name",
            "color",
            "location",
            "is_mr_x"
        }
        """
        p = self.__getPlayerByID(player_id)
        return {
            "game_id": self.__ID,
            "player_id": player_id,
            "name": p.name,
            "color": p.color,
            "location": p.location,
            "is_mr_x": p.is_mr_x
        }

    def setColor(self, player_id: str, color: str):
        if color not in self.__available_colors:
            raise ValueError("Color not available.")
        player = self.__getPlayerByID(player_id)
        if player.is_mr_x:
            raise RuntimeError("Cannot assign color to Mr. X.")
        oldColor = player.color
        player.color = color
        self.__available_colors.remove(color)
        self.__available_colors.append(oldColor)

    def setMrX(self, player_id: str):
        player = self.__getPlayerByID(player_id)
        oldX = self.__mrX
        oldX.is_mr_x = False
        player.is_mr_x = True
        self.__mrX = player
        oldX.color = player.color
        player.color = 'X'

    def addPlayer(self, player_id: str, player_name: str):
        """add a player to the game"""
        print(f"\tregistering {player_name}...")
        if len(self.__players) >= MAX_PLAYERS:
            raise RuntimeError("Game is full!")
        if player_id in self.__players:
            raise ValueError("player already connected")

        is_mr_x = not self.__players  # true when self.players is empty
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
        self.__players[player_id] = newPlayer

        print("\tdone.\ntotal players connected: " + str(len(self.__players)))

        self.__players[player_id] = newPlayer

    def removePlayer(self, player_id: str):
        """remove a player from the game"""
        if self.state == GameState.CONNECTING:
            raise RuntimeError(
                "Players will not be removed during CONNECTING state")
        player = self.__getPlayerByID(player_id)

        if self.state == GameState.RUNNING:
            self.end("player disconnected during game")

        print(f"removing player {player_id} from {self.ID}")

        if player.is_mr_x:
            newX = choice(self.__players)
            self.setMrX(newX)

        self.__available_colors.append(player.color)

        if self.state == GameState.PENDING:
            self.__available_locations.append(player.location)
        del self.__players[player_id]

    def start(self):
        if len(self.__players) != MAX_PLAYERS:
            raise RuntimeError(
                f"Invalid number of players: {len(self.__players)}")
        if self.state != GameState.PENDING:
            raise RuntimeError("Game alreaady started")

        self.state = GameState.RUNNING

    def end(self, reason: str = ""):
        """end the game, optionally specify reason"""
        self.state = GameState.STOPPED
        self.stop_reason = reason
        print(f"game ended: {reason}")

    def move(self, player_id: str, location: int, ticket: str):
        """perform a move"""
        if self.__cycle >= MOVE_LIMIT:
            raise RuntimeError(f"Game has finished {MOVE_LIMIT} cycles")
        player = self.__getPlayerByID(player_id)

        if(self.__isValidMove(player_id, location, ticket)):
            player.discard(ticket)
            player.location = location
            if not player.is_mr_x:
                self.__mrX.gain(ticket)
            self.__advanceTurn()
        else:
            raise ValueError("Invalid move.")
