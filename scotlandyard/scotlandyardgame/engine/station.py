class Station:
    """
    One location on the game board.
    """

    def __init__(self, loc: int) -> None:
        self.location = loc
        self.neighbours: dict[str, set[Station]] = {
            "taxi": set(),
            "bus": set(),
            "underground": set(),
            "special": set()
        }

    def getNeighbours(self, type: str) -> list[Station]:
        return self.neighbours[type]

    def addNeighbour(self, type: str, station: Station):
        self.neighbours[type].add(station)