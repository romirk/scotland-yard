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
        self.limits = {"min": [0, 0], "max": [0, 0]}

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
        print(f"done. limits: {self.limits}")

    def is_too_close(self, coords):
        for i in range(self.N):
            if self.stations[i].coords is not None:
                if np.linalg.norm(coords - self.stations[i].coords) < 1:
                    return True
        return False

    def generate_coordinates(self):

        multipliers = {
            TAXI_TICKET: 2,
            BUS_TICKET: 3,
            UNDERGROUND_TICKET: 5,
            BLACK_TICKET: 7,
        }

        visited = np.zeros(self.N, dtype=bool)
        q = [self.stations[0]]
        self.stations[0].coords = self.coords[0] = np.array((0, 0))

        while q:
            station = q.pop(0)
            visited[station.location] = True
            for ticket_type, neighbours in station.neighbours.items():

                phi = np.random.rand() * 2 * np.pi

                for i, neighbour in enumerate(neighbours):
                    if neighbour < self.N and not visited[neighbour]:

                        theta = i * 2 * np.pi / len(neighbours)
                        calculated_coords = np.array(
                            (
                                station.coords[0]
                                + multipliers[ticket_type] * np.cos(theta + phi),
                                station.coords[1]
                                + multipliers[ticket_type] * np.sin(theta + phi),
                            )
                        )

                        if self.stations[neighbour].coords is not None:
                            calculated_coords = (
                                calculated_coords + self.stations[neighbour].coords
                            ) / 2

                        while self.is_too_close(calculated_coords):
                            calculated_coords = np.array(
                                (
                                    calculated_coords[0] + (np.random.rand() - 0.5) * 2,
                                    calculated_coords[1] + (np.random.rand() - 0.5) * 2,
                                )
                            )

                        self.coords[neighbour] = self.stations[
                            neighbour
                        ].coords = calculated_coords

                        if calculated_coords[0] < self.limits["min"][0]:
                            self.limits["min"][0] = calculated_coords[0]
                        if calculated_coords[1] < self.limits["min"][1]:
                            self.limits["min"][1] = calculated_coords[1]
                        if calculated_coords[0] > self.limits["max"][0]:
                            self.limits["max"][0] = calculated_coords[0]
                        if calculated_coords[1] > self.limits["max"][1]:
                            self.limits["max"][1] = calculated_coords[1]

                        q.append(self.stations[neighbour])

    def coords_as_list(self):
        return [self.coords[i].tolist() for i in range(self.N)]


MAP = Map(MAP_DATA)
