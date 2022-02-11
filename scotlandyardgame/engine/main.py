from random import choice, randrange, shuffle
from typing import Final

from .constants import (
    AVAILABLE_COLORS,
    AVAILABLE_START_LOCATIONS,
    BLACK_TICKET,
    CYCLE_LIMIT,
    DOUBLE_TICKET,
    MAX_PLAYERS,
    SURFACE_MOVES,
    TICKET_TYPES,
    EndState,
    GameState,
)
from .map import MAP
from .player import Player


class ScotlandYard:
    """
    Instance of a ```ScotlandYard``` game. Stores all game information and handles game logic.
    """

    def __init__(self, id: str) -> None:
        # private
        self.__ID: Final[str] = id
        self.__players: dict[str, Player] = {}
        self.__order: list[str] = []

        self.__available_start_locations: list[int] = AVAILABLE_START_LOCATIONS.copy()
        self.__available_colors: list[str] = AVAILABLE_COLORS.copy()

        # cycle = everyone gets 1 turn
        self.__turn: int = 0
        self.__cycle: int = 0
        self.__is_stagnant_cycle: bool = True

        # public
        self.state: GameState = GameState.PENDING
        self.rollCall: set[str] = set()
        self.moveLog: list[dict] = []

    # getters

    @property
    def id(self) -> str:
        return self.__ID

    # setters

    @id.setter
    def id(self, *args):
        raise AttributeError("ID assignment not allowed.")

    # private methods

    def __is_valid_move(self, player_id: str, location: int, ticket: str) -> bool:
        """checks if player with ```player_id``` can move to ```location``` using ```ticket```"""
        player = self.__get_player_by_id(player_id)

        return (
            player is not None
            and (ticket != BLACK_TICKET or player.is_mr_x)
            and player.tickets.get(ticket) > 0
            and location in MAP.stations[player.location].getNeighbours(ticket)
            and (
                self.__get_player_at(location) is None
                or (
                    not player.is_mr_x and self.__get_player_at(location) == self.__mr_x
                )
            )
        )

    def __is_mr_x_caught(self) -> bool:
        """checks if game is over"""
        for player in self.__players.values():
            if player.location == self.__mr_x.location and not player.is_mr_x:
                return True

        return False

    def __check_win_condition(self) -> EndState:
        """checks if game is over"""
        if self.state == GameState.STOPPED:
            return self.stop_reason
        if not self.__turn and self.__is_stagnant_cycle:
            return EndState.MR_X_WINS
        if self.__cycle >= CYCLE_LIMIT:
            return EndState.MR_X_WINS
        if self.__is_mr_x_caught():
            return EndState.DETECTIVES_WIN
        return EndState.NOT_ENDED

    def __get_player_by_id(self, playerID: str) -> Player:
        """returns ```Player``` in current game with ID ```playerID```"""
        if playerID not in self.__players:
            raise ValueError("player does not exist in this game")
        return self.__players[playerID]

    def __get_player_at(self, loc: int) -> Player:
        """returns ```Player``` in current game with location ```loc```"""
        for player in self.__players.values():
            if player.location == loc:
                return player

    def __move(self, player: Player, ticket: str, location: int):
        """moves player to ```location``` using ```ticket```"""
        if not self.__is_valid_move(player.id, location, ticket):
            raise ValueError("Invalid move")
        player.location = location
        player.tickets.discard(ticket)
        if not player.is_mr_x:
            self.__mr_x.tickets.gain(ticket)

    def __double_move(
        self, player: Player, ticket1: str, location1: int, ticket2: str, location2: int
    ):
        """performs a double move"""
        if not player.is_mr_x:
            raise ValueError("Only Mr. X can double move")

        old_location = player.location
        old_tickets = player.tickets.all()
        try:
            self.__move(player, ticket1, location1)
            self.__move(player, ticket2, location2)
            player.tickets.discard(DOUBLE_TICKET)
        except ValueError as e:
            player.location = old_location
            player.tickets.set(old_tickets)
            raise e

    def __advance_turn(self):
        """called at the end of move to advance turn"""
        self.__turn = (self.__turn + 1) % 6
        if not self.__turn:
            self.__cycle += 1

    # public methods

    def is_boxed_in(self, player_id: str):
        """checks if player is boxed in"""
        player = self.__get_player_by_id(player_id)
        for ticket in TICKET_TYPES:
            if ticket == BLACK_TICKET and not player.is_mr_x:
                continue
            neighbours = MAP.stations[player.location].getNeighbours(ticket)
            for neighbour in neighbours:
                if self.__is_valid_move(player_id, neighbour, ticket):
                    return False
        return True

    def get_host_id(self) -> str:
        """returns the ID of the game host"""
        return self.__host.id

    def get_player_ids(self) -> list[str]:
        """Get a list of connected player IDs"""
        return [p for p in self.__players]

    def get_player_names(self) -> list[str]:
        """Get a list of connected player names"""
        return [p.name for p in self.__players.values()]

    def get_player_info(self, player_id: str) -> dict:
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
        if player_id == "ALL":
            info = {p: self.get_player_info(p) for p in self.__players.keys()}
            del info[self.__mr_x.id]["location"]
            return info

        p = self.__get_player_by_id(player_id)
        return {
            "game_id": self.__ID,
            "player_id": player_id,
            "name": p.name,
            "color": p.color,
            "location": p.location,
            "tickets": p.tickets.all(),
            "is_host": p.id == self.get_host_id(),
        }

    def get_game_info(self) -> dict:
        """get information about the current game"""
        return {
            "game_id": self.id,
            "state": str(self.state),
            "host_id": self.__host.id,
            "move_order": self.__order,
            "cycle": self.__cycle,
            "turn": self.__turn,
            "mr_x_ticket_log": [
                (
                    move["ticket"]
                    if move["ticket"] != DOUBLE_TICKET
                    else f'double {move["double_tickets"][0]} {move["double_tickets"][1]}'
                )
                for move in self.moveLog
                if move["is_mr_x"]
            ],
        }

    def get_mr_x(self) -> str:
        """returns the ID of Mr. X"""
        return self.__mr_x.id if self.__mr_x is not None else None

    def get_whose_turn(self) -> str:
        """return player ID of the player whose turn it currently is"""
        if not self.__turn:
            return self.__mr_x.id
        else:
            self.__order[self.__turn - 1]

    def set_color(self, player_id: str, color: str):
        """set player color"""
        player = self.__get_player_by_id(player_id)
        if color == player.color:
            return
        if color not in self.__available_colors:
            raise ValueError("Color not available.")
        if player.is_mr_x:
            raise RuntimeError("Cannot assign color to Mr. X.")
        old_color = player.color
        player.color = color
        self.__available_colors.remove(color)
        self.__available_colors.append(old_color)

    def set_mr_x(self, player_id: str):
        """set a player to Mr. X, unsetting the previous Mr. X, if they exist"""
        if self.state == GameState.RUNNING:
            raise RuntimeError("Game already started")

        player = self.__get_player_by_id(player_id)
        old_x = self.__mr_x

        if old_x is not None:
            old_x.color = player.color

        self.__mr_x = player
        player.color = "X"

    def add_player(self, player_id: str, player_name: str):
        """add a player to the game"""
        print(f"\tregistering {player_name}...")
        if self.state != GameState.PENDING:
            if self.state == GameState.STOPPED:
                raise RuntimeError("Game has ended")
            else:
                raise RuntimeError("Game already started")
        if len(self.__players) >= MAX_PLAYERS:
            raise RuntimeError("Game is full!")
        if player_id in self.__players:
            raise ValueError("player already connected")

        is_host = not len(self.__players)  # true when self.players is empty
        print(f"\t\thost: {is_host}")

        if is_host:
            col = "X"
        else:
            col_index = randrange(len(self.__available_colors))
            col = self.__available_colors[col_index]
            del self.__available_colors[col_index]

        print(f"\t\tcolor: {col}")

        loc_index = randrange(len(self.__available_start_locations))
        loc = self.__available_start_locations[loc_index]
        del self.__available_start_locations[loc_index]

        print(f"\t\tlocation: {loc}")

        new_player = Player(player_id, player_name, loc, col)

        self.__players[player_id] = new_player

        print("\tdone.\ntotal players connected: " + str(len(self.__players)))

        self.__players[player_id] = new_player

        if is_host:
            self.__mr_x = self.__host = new_player

    def remove_player(self, player_id: str):
        """remove a player from the game"""
        if self.state == GameState.CONNECTING:
            raise RuntimeError("Players will not be removed during CONNECTING state")

        player = self.__get_player_by_id(player_id)
        is_x = player.is_mr_x
        is_host = player.id == self.get_host_id()

        # if player is removed during gameplay, end the game
        if self.state == GameState.RUNNING:
            self.end(EndState.ABORTED)

        print(f"removing player {player_id} from {self.id}")

        if player.color != "X":
            self.__available_colors.append(player.color)

        if self.state == GameState.PENDING:
            self.__available_start_locations.append(player.location)
        del self.__players[player_id]

        if not len(self.__players):
            self.end(EndState.ABORTED)
            return

        if is_x:
            new_x_id = choice(tuple(self.__players.keys()))
            self.__mr_x = self.__get_player_by_id(new_x_id)
            self.set_mr_x(self.__mr_x.id)

        if is_host:
            new_host_id = choice(tuple(self.__players.keys()))
            self.__host = self.__get_player_by_id(new_host_id)

    def start(self):
        """do precondition checks and start game"""
        if len(self.__players) != MAX_PLAYERS:
            raise RuntimeError(f"Invalid number of players: {len(self.__players)}")
        if self.state != GameState.CONNECTING:
            return
        if self.rollCall != set(self.get_player_ids()):
            raise RuntimeError("Roll call doesn't match players")

        print("starting game...")

        detectives = self.get_player_ids()
        detectives.remove(self.__mr_x.id)
        shuffle(detectives)
        self.__order = [self.__mr_x.id] + detectives

        self.state = GameState.RUNNING
        print("running.")

    def end(self, reason: EndState = EndState.ABORTED):
        """end the game, optionally specify reason"""
        self.state = GameState.STOPPED
        self.stop_reason = reason
        print(f"game ended: {reason}")

    def request_move(self, player_id: str, ticket: str, data: dict):
        """perform a move"""
        player = self.__get_player_by_id(player_id)

        if self.__order[self.__turn] != player_id:
            return {"accepted": False, "message": "Not your turn"}

        if not self.__turn:
            self.__is_stagnant_cycle = True

        try:
            if ticket == DOUBLE_TICKET:
                self.__double_move(
                    player,
                    data["ticket1"],
                    data["location1"],
                    data["ticket2"],
                    data["location2"],
                )
            elif ticket == "pass":
                if not self.is_boxed_in(player_id):
                    raise ValueError("Making a move is possible")
                if player.is_mr_x:
                    self.end(EndState.DETECTIVES_WIN)
            else:
                self.__move(player, ticket, data["location"])
                if not player.is_mr_x:
                    self.__is_stagnant_cycle = False
        except ValueError as e:
            print(e)
            return {"accepted": False, "message": str(e)}

        move = {
            "accepted": True,
            "player_id": player_id,
            "destination": player.location,
            "ticket": ticket,
            "is_mr_x": player.is_mr_x,
            "is_surface_move": self.__cycle in SURFACE_MOVES,
            "cycle_number": self.__cycle,
            "game_state": self.state,
        }

        if ticket == DOUBLE_TICKET:
            move["double_tickets"] = (data["ticket1"], data["ticket2"])
            move["double_locations"] = (data["location1"], data["location2"])

        self.__advance_turn()
        end_state = self.__check_win_condition()

        if end_state != EndState.NOT_ENDED:
            self.end(end_state)
            move["game_state"] = end_state

        self.moveLog.append(move)
        return move
