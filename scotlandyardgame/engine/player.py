from scotlandyardgame.engine.constants import Ticket


class Player:

    def __init__(self, player_id: str, player_name: str, player_location: int, player_color: str) -> None:
        # private
        self.__ID: str = player_id
        self.__player_location: int = player_location
        self.__tickets: dict[Ticket, int] = {
            Ticket.TAXI: 4,
            Ticket.BUS: 3,
            Ticket.UNDERGROUND: 3,
            Ticket.BLACK: 5,
            Ticket.DOUBLE: 2
        } if player_color == 'X' else {
            Ticket.TAXI: 10,
            Ticket.BUS: 8,
            Ticket.UNDERGROUND: 4
        }

        # public
        self.name: str = player_name
        self.color: str = player_color

    # getters

    @property
    def ID(self) -> str:
        return self.__ID

    @property
    def location(self) -> int:
        return self.__player_location

    @property
    def is_mr_x(self) -> bool:
        return self.color == 'X'

    # setters

    @ID.setter
    def ID(self, newID: str):
        raise AttributeError("ID assignment not allowed.")

    @location.setter
    def location(self, newLocation: int):
        self.__player_location = newLocation if 1 <= newLocation <= 200 else self.__player_location

    # methods
    def getTickets(self, type: Ticket) -> int:
        """returns number of tickets of type ```type``` available to this player."""
        return self.__tickets[type]

    def getAllTickets(self) -> dict[Ticket, int]:
        return self.__tickets.copy()

    def discard(self, type: Ticket):
        """player uses a ticket."""
        self.__tickets[type] -= 1 if self.__tickets[type] else 0

    def gain(self, type: Ticket):
        if not self.is_mr_x:
            raise TypeError("non-Mr. X Player cannot gain a ticket.")
        if type not in [Ticket.TAXI, Ticket.BUS, Ticket.UNDERGROUND]:
            raise ValueError(f"cannot gain ticket of type '{type}.'")
        self.__tickets[type] += 1
