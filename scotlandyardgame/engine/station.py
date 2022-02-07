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
        self.coords = None

    def getNeighbours(self, ticket_type: str) -> set[int]:
        return self.neighbours[ticket_type]

    def getAllNeighbours(self) -> set[int]:
        return set.union(*self.neighbours.values())

    def addNeighbour(self, ticket_type: str, station: int):
        self.neighbours[ticket_type].add(station)

    def __lt__(self, other):
        return self.location < other.location
