from scotlandyardgame.engine.constants import Ticket


class Station:
    """
    One location on the game board.
    """

    def __init__(self, loc: int) -> None:
        self.location = loc
        self.neighbours: dict[str, set[int]] = {
            "taxi": set(),
            "bus": set(),
            "underground": set(),
            "black": set()
        }

    def getNeighbours(self, ticket_type: Ticket) -> set[int]:
        return self.neighbours[str(ticket_type)[7:].lower()]

    def addNeighbour(self, ticket_type: Ticket, station: int):
        self.neighbours[str(ticket_type)[7:].lower()].add(station)