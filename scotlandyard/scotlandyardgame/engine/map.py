from station import Station

class Map:
    """
    Map of the game board.
    """
    def __init__(self, mapdata: list[list[list[int]]] = []) -> None:
        self.__N = len(mapdata)
        self.__stations: Station = []