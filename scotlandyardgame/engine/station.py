from .constants import BLACK_TICKET, BUS_TICKET, TAXI_TICKET, UNDERGROUND_TICKET


class Station:
    """
    One location on the game board.
    """

    def __init__(self, loc: int) -> None:
        self.location = loc
        self.neighbours: dict[str, set[int]] = {
            TAXI_TICKET: set(),
            BUS_TICKET: set(),
            UNDERGROUND_TICKET: set(),
            BLACK_TICKET: set(),
        }

    def getNeighbours(self, ticket_type: str) -> set[int]:
        """gets all neighbours of this station that are reachable by the given ticket type"""
        return self.neighbours[ticket_type]

    def addNeighbour(self, ticket_type: str, station: int):
        """adds a neighbour to this station"""
        self.neighbours[ticket_type].add(station)
