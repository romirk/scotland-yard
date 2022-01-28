from .station import Station
from .constants import TICKET_TYPES



class Map:
    """
    Map of the game board.
    """

    def __init__(self, mapdata: list[list[list[int]]] = []) -> None:
        print("initializing map")
        self.N = len(mapdata)
        self.stations: list[Station] = []

        for index in range(self.N):
            station = Station(index)
            for type in range(len(mapdata[index])):
                for neighbour in range(len(mapdata[index][type])):
                    station.addNeighbour(
                        TICKET_TYPES[type], mapdata[index][type][neighbour] - 1)
            self.stations.append(station)
