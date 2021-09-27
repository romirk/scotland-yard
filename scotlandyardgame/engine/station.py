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

    def getNeighbours(self, type: str) -> set[int]:
        return self.neighbours[type]

    def addNeighbour(self, type: str, station: int):
        self.neighbours[type].add(station)