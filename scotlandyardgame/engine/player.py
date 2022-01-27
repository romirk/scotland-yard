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
    def getTickets(self, ticket_type: Ticket|str) -> int:
        """returns number of tickets of type ```type``` available to this player."""
        return self.__tickets[Ticket.fromStr(ticket_type)]

    def setTickets(self, tickets: dict[Ticket, int]):
        """set the tickets for this player"""
        self.__tickets = tickets

    def getAllTickets(self) -> dict[str, int]:
        """returns all tickets available to this player."""
        return {
            "taxi": self.__tickets[Ticket.TAXI],
            "bus": self.__tickets[Ticket.BUS],
            "underground": self.__tickets[Ticket.UNDERGROUND],
            "black": self.__tickets[Ticket.BLACK],
            "double": self.__tickets[Ticket.DOUBLE]
        } if self.color == 'X' else {
            "taxi": self.__tickets[Ticket.TAXI],
            "bus": self.__tickets[Ticket.BUS],
            "underground": self.__tickets[Ticket.UNDERGROUND],
        }

    def discard(self, ticket_type: Ticket):
        """player uses a ticket."""
        self.__tickets[Ticket.fromStr(ticket_type)] -= 1 if self.__tickets[Ticket.fromStr(ticket_type)] else 0

    def gain(self, type: Ticket):
        """Mr. X gains a ticket"""
        type = Ticket.fromStr(type)
        if not self.is_mr_x:
            raise TypeError("non-Mr. X Player cannot gain a ticket.")
        if type not in [Ticket.TAXI, Ticket.BUS, Ticket.UNDERGROUND]:
            raise ValueError(f"cannot gain ticket of type '{type}.'")
        self.__tickets[type] += 1
