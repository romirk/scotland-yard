from random import choice, randrange, shuffle
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

        self.__available_start_locations: list[int] = AVAILABLE_START_LOCATIONS.copy(
        )
        self.__available_colors: list[str] = AVAILABLE_COLORS.copy()

        # cycle = everyone gets 1 turn
        self.__turn: int = 0
        self.__cycle: int = 0
        self.__mrX: Player = None
        self.__host: Player = None

        # public
        self.state: GameState = GameState.PENDING
        self.rollCall: set[str] = set()
        self.moveLog: list[dict] = []

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
                and (ticket != Ticket.BLACK or player.is_mr_x)
                and player.getTickets(ticket) > 0
                and location in MAP.stations[player.location].getNeighbours(ticket)
                and (self.__getPlayerAt(location) is None
                     or (not player.is_mr_x and self.__getPlayerAt(location) == self.__mrX)))

    def __move(self, player: Player, ticket: Ticket, location: int):
        if not self.__isValidMove(player.ID, location, ticket):
            raise ValueError("Invalid move")
        player.location = location
        player.discard(ticket)
        if not player.is_mr_x:
            self.__mrX.gain(ticket)

    def __doubleMove(self, player: Player, ticket1: Ticket, location1: int, ticket2: Ticket, location2: int):
        old_location = player.location
        old_tickets = player.getAllTickets()
        try:
            self.__move(player, ticket1, location1)
            self.__move(player, ticket2, location2)
        except ValueError as e:
            player.location = old_location
            player.setTickets(old_tickets)
            raise e

    def __checkEndState(self) -> EndState:
        """checks if game is over"""

        if self.__cycle >= CYCLE_LIMIT:
            return EndState.MR_X_WINS

        for player in self.__players.values():
            if player.location == self.__mrX.location and not player.is_mr_x:
                return EndState.DETECTIVES_WIN

        return EndState.NOT_ENDED

    def __advanceTurn(self):
        """called at the end of move to advance turn"""
        self.__turn = (self.__turn + 1) % 6
        if not self.__turn:
            self.__cycle += 1
        if self.__cycle >= CYCLE_LIMIT:
            self.end(EndState.MR_X_WINS)

    # public methods

    def getHostID(self) -> str:
        """returns the ID of the game host"""
        return self.__host.ID

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
            "is_host"
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
            "is_host": p.ID == self.getHostID()
        }

    def getGameInfo(self) -> dict:
        return {
            "game_id": self.ID,
            "state": str(self.state),
            "host_id": self.__host.ID,
            "player_info": [self.getPlayerInfo(p) for p in self.__players.keys()],
            "move_order": self.__order,
            "cycle": self.__cycle,
            "turn": self.__turn,
            "mr_x_ticket_log": [move['ticket'] for move in self.moveLog if move["is_mr_x"]],
        }

    def getMrX(self) -> str:
        """returns the ID of Mr. X"""
        return self.__mrX.ID if self.__mrX is not None else None

    def getWhoseTurn(self) -> str:
        """return player ID of the player whose turn it currently is"""
        if not self.__turn:
            return self.__mrX.ID
        else:
            self.__order[self.__turn - 1]

    def setColor(self, player_id: str, color: str):
        """set player color"""
        player = self.__getPlayerByID(player_id)
        if color == player.color:
            return
        if color not in self.__available_colors:
            raise ValueError("Color not available.")
        if player.is_mr_x:
            raise RuntimeError("Cannot assign color to Mr. X.")
        oldColor = player.color
        player.color = color
        self.__available_colors.remove(color)
        self.__available_colors.append(oldColor)

    def setMrX(self, player_id: str):
        """set a player to Mr. X, unsetting the previous Mr. X, if they exist"""
        if self.state == GameState.RUNNING:
            raise RuntimeError("Game already started")

        player = self.__getPlayerByID(player_id)
        oldX = self.__mrX

        if oldX is not None:
            oldX.color = player.color

        self.__mrX = player
        player.color = 'X'

    def addPlayer(self, player_id: str, player_name: str):
        """add a player to the game"""
        print(f"\tregistering {player_name}...")
        if self.state != GameState.PENDING:
            raise RuntimeError("Game already started")
        if len(self.__players) >= MAX_PLAYERS:
            raise RuntimeError("Game is full!")
        if player_id in self.__players:
            raise ValueError("player already connected")

        is_host = not len(self.__players)  # true when self.players is empty
        print(f"\t\thost: {is_host}")

        if is_host:
            col = 'X'
        else:
            col_index = randrange(len(self.__available_colors))
            col = self.__available_colors[col_index]
            del self.__available_colors[col_index]

        print(f"\t\tcolor: {col}")

        loc_index = randrange(len(self.__available_start_locations))
        loc = self.__available_start_locations[loc_index]
        del self.__available_start_locations[loc_index]

        print(f"\t\tlocation: {loc}")

        newPlayer = Player(player_id, player_name, loc, col)

        self.__players[player_id] = newPlayer

        print("\tdone.\ntotal players connected: " + str(len(self.__players)))

        self.__players[player_id] = newPlayer

        if is_host:
            self.__mrX = self.__host = newPlayer

    def removePlayer(self, player_id: str):
        """remove a player from the game"""
        if self.state == GameState.CONNECTING:
            raise RuntimeError(
                "Players will not be removed during CONNECTING state")

        player = self.__getPlayerByID(player_id)
        isX = player.is_mr_x
        isHost = player.ID == self.getHostID()

        # if player is removed during gameplay, end the game
        if self.state == GameState.RUNNING:
            self.end(EndState.ABORTED)

        print(f"removing player {player_id} from {self.ID}")

        self.__available_colors.append(player.color)

        if self.state == GameState.PENDING:
            self.__available_start_locations.append(player.location)
        del self.__players[player_id]

        if not len(self.__players):
            self.end(EndState.ABORTED)
            return

        if isX:
            newXID = choice(tuple(self.__players.keys()))
            self.__mrX = self.__getPlayerByID(newXID)
            self.setMrX(self.__mrX.ID)

        if isHost:
            newHostID = choice(tuple(self.__players.keys()))
            self.__host = self.__getPlayerByID(newHostID)

    def start(self):
        """do precondition checks and set gamestate"""
        if len(self.__players) != MAX_PLAYERS:
            raise RuntimeError(
                f"Invalid number of players: {len(self.__players)}")
        if self.state != GameState.PENDING:
            return
        if self.rollCall != set(self.getPlayerIDs()):
            raise RuntimeError("Roll call doesn't match players")

        detectives = self.getPlayerIDs().remove(self.__mrX.ID)
        shuffle(detectives)
        self.__order = [self.__mrX.ID] + detectives

        self.state = GameState.RUNNING

    def end(self, reason: EndState = EndState.ABORTED):
        """end the game, optionally specify reason"""
        self.state = GameState.STOPPED
        self.stop_reason = reason
        print(f"game ended: {reason}")

    def requestMove(self, player_id: str, ticket: Ticket, data: dict):
        """perform a move"""

        player = self.__getPlayerByID(player_id)

        if ticket == Ticket.DOUBLE:
            if not player.is_mr_x:
                raise ValueError("Only Mr. X can use DOUBLE")
            self.__doubleMove(
                player, data["ticket1"], data["location1"], data["ticket2"], data["location2"])
        else:
            self.__move(player, ticket, data["location"])

        self.__advanceTurn()
        end_state = self.__checkEndState()
        if end_state is not EndState.NOT_ENDED:
            self.end(end_state)

        move = {
            "player_id": player_id,
            "destinaiton": player.location,
            "ticket": ticket,
            "is_mr_x": player.is_mr_x,
            "is_surface_move": self.__cycle in SURFACE_MOVES,
            "double_tickets": (data["ticket1"],data["ticket2"]) if ticket == Ticket.DOUBLE else None,
            "double_locations":  (data["location1"],data["location2"]) if ticket == Ticket.DOUBLE else None,
            "cycle_number": self.__cycle
        }

        self.moveLog.append(move)
        return move