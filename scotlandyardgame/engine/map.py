from scotlandyardgame.engine.mapdata import MAP_DATA
from .station import Station
from .constants import (
    BLACK_TICKET,
    BUS_TICKET,
    TAXI_TICKET,
    TICKET_TYPES,
    UNDERGROUND_TICKET,
)
import numpy as np


class Map:
    """
    Map of the game board.
    """

    def __init__(self, map_data: list[list[list[int]]] = []) -> None:
        print("building map...")
        self.N = len(map_data)
        self.map_data = map_data
        self.stations: list[Station] = []
        self.coords: dict[int, np.ndarray] = dict()

        for index in range(self.N):
            station = Station(index)
            for type in range(len(map_data[index])):
                for neighbour in range(len(map_data[index][type])):
                    station.addNeighbour(
                        TICKET_TYPES[type], map_data[index][type][neighbour] - 1
                    )
            self.stations.append(station)
        print("initialized map with", self.N, "stations.\ngenerating coordinates...")
        self.generate_coordinates()
        print("done.")

    def is_too_close(self, station_index):
        for i in range(self.N):
            if i != station_index and self.stations[i].coords is not None:
                if (
                    np.linalg.norm(
                        self.stations[station_index].coords - self.stations[i].coords
                    )
                    < 0.5
                ):
                    return True
        return False

    def generate_coordinates(self):
        visited = np.zeros(self.N, dtype=bool)
        q = [self.stations[0]]
        self.stations[0].coords = self.coords[0] = np.array((0, 0))
        type_multipliers = {
            TAXI_TICKET: 2,
            BUS_TICKET: 3,
            UNDERGROUND_TICKET: 5,
            BLACK_TICKET: 7,
        }

        while q:
            station = q.pop(0)
            visited[station.location] = True
            for ticket_type, neighbours in station.neighbours.items():
                for i, neighbour in enumerate(neighbours):
                    if neighbour < self.N and not visited[neighbour]:

                        calculated_coords = np.array(
                            (
                                station.coords[0]
                                + type_multipliers[ticket_type]
                                * np.cos(i * 2 * np.pi / len(neighbours)),
                                station.coords[1]
                                + type_multipliers[ticket_type]
                                * np.sin(i * 2 * np.pi / len(neighbours)),
                            )
                        )

                        if self.stations[neighbour].coords is None:
                            self.stations[neighbour].coords = calculated_coords
                        else:
                            self.stations[neighbour].coords = (
                                calculated_coords + self.stations[neighbour].coords
                            ) / 2

                        self.coords[neighbour] = self.stations[neighbour].coords

                        while self.is_too_close(neighbour):
                            self.stations[neighbour].coords = np.array(
                                (
                                    self.stations[neighbour].coords[0]
                                    + 2 * np.random.rand(),
                                    self.stations[neighbour].coords[1]
                                    + 2 * np.random.rand(),
                                )
                            )
                            self.coords[neighbour] = self.stations[neighbour].coords

                        q.append(self.stations[neighbour])

    def coords_as_list(self):
        return [self.coords[i].tolist() for i in range(self.N)]


MAP = Map(MAP_DATA)
