from scotlandyardgame.engine.constants import Ticket


class Station:
    """
    One location on the game board.
    """

    def __init__(self, loc: int) -> None:
        self.location = loc
        self.neighbours: dict[str, set[int]] = {
            Ticket.TAXI: set(),
            Ticket.BUS: set(),
            Ticket.UNDERGROUND: set(),
            Ticket.BLACK: set()
        }

    def getNeighbours(self, ticket_type: Ticket) -> set[int]:
        n = self.neighbours[Ticket.fromStr(ticket_type)]
        print(type(ticket_type), type(Ticket.fromStr(ticket_type)), n)
        return n

    def addNeighbour(self, ticket_type: Ticket, station: int):
        self.neighbours[Ticket.fromStr(ticket_type)].add(station)
