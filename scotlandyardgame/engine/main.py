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
        self.__order: list[str] = []

        self.__available_locations: list[int] = AVAILABLE_MOVES.copy()
        self.__available_colors: list[str] = AVAILABLE_COLORS.copy()

        # cycle = everyone gets 1 move
        self.__moves: int = 0
        self.__cycle: int = 0
        self.__mrX: Player = None

        # public
        self.state: GameState = GameState.PENDING
        self.rollCall: set[str] = set()

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
        for player in self.__players.values():
            if player.location == loc:
                return player

    def __isValidMove(self, player_id: str, location: int, ticket: Ticket) -> bool:
        """checks if player with ```player_id``` can move to ```location``` using ```ticket```"""
        player = self.__getPlayerByID(player_id)
        return (player is not None
                and (ticket not in [Ticket.BLACK, Ticket.DOUBLE] or player.is_mr_x)
                and player.getTickets(ticket) > 0
                and location in MAP.stations[player.location].getNeighbours(ticket)
                and (self.__getPlayerAt(location) is None
                     or (not player.is_mr_x and self.__getPlayerAt(location) == self.__mrX)))

    def __advanceTurn(self):
        """called at the end of move to advance turn"""
        self.__moves = (self.__moves + 1) % 6
        if not self.__moves:
            self.__cycle += 1
        if self.__cycle >= CYCLE_LIMIT:
            self.end(EndState.MR_X_WINS)

    # public methods

    def getPlayerIDs(self) -> list[str]:
        """Get a list of connected player IDs"""
        return [p for p in self.__players]

    def getPlayerNames(self) -> list[str]:
        """Get a list of connected player names"""
        return [p.name for p in self.__players.values()]

    def getPlayerInfo(self, player_id: str) -> dict:
        """
        returns a ```dict``` containing information about a specified player

        {
            "game_id",
            "player_id",
            "name",
            "color",
            "location",
            "tickets",
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
            "tickets": p.getAllTickets(),
            "is_mr_x": p.is_mr_x
        }

    def getMrX(self) -> str:
        """returns the ID of Mr. X"""
        return self.__mrX.ID if self.__mrX is not None else None

    def getWhoseTurn(self) -> str:
        """return player ID of the player whose turn it currently is"""
        if not self.__moves:
            return self.__mrX.ID
        else:
            self.__order[self.__moves - 1]

    def setColor(self, player_id: str, color: str):
        """set player color"""
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
        """set a player to Mr. X, unsetting the previous Mr. X, if they exist"""
        player = self.__getPlayerByID(player_id)
        oldX = self.__mrX

        if oldX is not None:
            oldX.color = player.color
            if self.__order:
                self.__order.insert(randrange(len(self.__order)), oldX.ID)
            else:
                self.__order.append(oldX.ID)

        self.__mrX = player
        player.color = 'X'
        self.__order.remove(player.ID)

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

        newPlayer = Player(player_id, player_name, loc, col)

        self.__players[player_id] = newPlayer
        if self.__order:
            self.__order.insert(randrange(len(self.__order)), newPlayer.ID)
        else:
            self.__order.append(newPlayer.ID)

        print("\tdone.\ntotal players connected: " + str(len(self.__players)))

        self.__players[player_id] = newPlayer

        if is_mr_x:
            self.__mrX = newPlayer

    def removePlayer(self, player_id: str):
        """remove a player from the game"""
        if self.state == GameState.CONNECTING:
            raise RuntimeError(
                "Players will not be removed during CONNECTING state")

        player = self.__getPlayerByID(player_id)
        isX = player.is_mr_x

        if self.state == GameState.RUNNING:
            self.end(EndState.ABORTED)

        print(f"removing player {player_id} from {self.ID}")

        self.__available_colors.append(player.color)

        if self.state == GameState.PENDING:
            self.__available_locations.append(player.location)
        del self.__players[player_id]
        self.__order.remove(player_id)

        if isX:
            if len(self.__players):
                self.__mrX = choice(self.__players)
                self.setMrX(self.__mrX.ID)
            else:
                self.__mrX = None

    def start(self):
        """do precondition checks and set gamestate"""
        if len(self.__players) != MAX_PLAYERS:
            raise RuntimeError(
                f"Invalid number of players: {len(self.__players)}")
        if self.state != GameState.PENDING:
            raise RuntimeError("Game alreaady started")
        if self.rollCall != set(self.getPlayerIDs()):
            raise RuntimeError("Roll call doesn't match players")

        self.state = GameState.RUNNING

    def end(self, reason: EndState):
        """end the game, optionally specify reason"""
        self.state = GameState.STOPPED
        self.stop_reason = reason
        print(f"game ended: {reason}")

    def move(self, player_id: str, location: int, ticket: Ticket):
        """perform a move"""
        if self.__cycle >= CYCLE_LIMIT:
            self.end(EndState.MR_X_WINS)
            raise RuntimeError(f"Game has finished {CYCLE_LIMIT} cycles")

        player = self.__getPlayerByID(player_id)

        if player_id != self.getWhoseTurn():
            raise RuntimeError("Not this player's turn")

        if not self.__isValidMove(player_id, location, ticket):
            raise ValueError("Invalid move.")

        player.discard(ticket)

        if not player.is_mr_x and self.__getPlayerAt(location) == self.__mrX:
            # game over
            self.end(EndState.DETECTIVES_WIN)
            return

        player.location = location
        if not player.is_mr_x:
            self.__mrX.gain(ticket)

        self.__advanceTurn()
