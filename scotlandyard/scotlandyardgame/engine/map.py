from _typeshed import Self
from station import Station

class Map:
    """
    Map of the game board.
    """
    def __init__(self, mapdata: list[list[list[int]]] = []) -> None:
        self.N = len(mapdata)
        self.stations: Station = []

        for i in range(self.__N):
            station = Station(i)
            for j in range(len(mapdata[i])): station.addNeighbour(j, mapdata[i][j] - 1)
            self.__stations.append(station)