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

        self.sub_graphs = {
            TAXI_TICKET: set(),
            BUS_TICKET: set(),
            UNDERGROUND_TICKET: set(),
            BLACK_TICKET: set(),
        }

        for index in range(self.N):
            station = Station(index)
            for type in range(len(map_data[index])):
                for neighbour in range(len(map_data[index][type])):
                    station.addNeighbour(
                        TICKET_TYPES[type], map_data[index][type][neighbour] - 1
                    )
                    self.sub_graphs[TICKET_TYPES[type]].add(
                        map_data[index][type][neighbour] - 1
                    )
            self.stations.append(station)


        print("initialized map with", self.N, "stations.\ngenerating coordinates...")
        self.generate_coordinates()
        print(f"limits: {self.limits}")

    def is_too_close(self, coords):
        for i in range(self.N):
            if i in self.coords:
                if np.linalg.norm(coords - self.coords[i]) < 1:
                    return True
        return False

    def generate_board_rectangular(self, shape):
        size = np.product(shape)
        board = np.zeros(size, dtype=int)
        i = np.sort(np.random.choice(np.arange(size), self.N, replace=False))
        board[i] = np.arange(1, 201)
        return board.reshape(shape)

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
            progress = int(np.count_nonzero(visited) / len(visited) * 10)
            print(f"[BFS] [{progress * '=' + (10 - progress) * ' '}]", end="\r")
            station = q.pop(0)
            visited[station.location] = True
            for ticket_type, neighbours in station.neighbours.items():

                phi = np.random.rand() * 2 * np.pi

                for i, neighbour in enumerate(neighbours):
                    if neighbour < self.N and not visited[neighbour]:

                        theta = i * 2 * np.pi / len(neighbours)
                        calculated_coords = np.array(
                            (
                                self.coords[station.location][0]
                                + multipliers[ticket_type] * np.cos(theta + phi),
                                self.coords[station.location][1]
                                + multipliers[ticket_type] * np.sin(theta + phi),
                            )
                        )

                        if neighbour in self.coords:
                            calculated_coords = (
                                calculated_coords + self.coords[neighbour]
                            ) / 2

                        while self.is_too_close(calculated_coords):
                            calculated_coords = np.array(
                                (
                                    calculated_coords[0] + (np.random.rand() - 0.5) * 2,
                                    calculated_coords[1] + (np.random.rand() - 0.5) * 2,
                                )
                            )

                        self.coords[neighbour] = station.coords = calculated_coords

                        if calculated_coords[0] < self.limits["min"][0]:
                            self.limits["min"][0] = calculated_coords[0]
                        if calculated_coords[1] < self.limits["min"][1]:
                            self.limits["min"][1] = calculated_coords[1]
                        if calculated_coords[0] > self.limits["max"][0]:
                            self.limits["max"][0] = calculated_coords[0]
                        if calculated_coords[1] > self.limits["max"][1]:
                            self.limits["max"][1] = calculated_coords[1]

                        q.append(self.stations[neighbour])
        print("[BFS] done.                                  ")

    def generate():

        """
unentangled graph psuedocode

        if no points are placed:
	place anywhere
else:
	[do not adjust placement if conditions are already satisified; in such cases, continue loop (or average position of all iterations)]
	for every cycle:
		
		if current point is connected to cycle
			compute centroid of cycle
			if current point is connected to all points in cycle, place at centroid
			else:
				compute theta = theta_max - theta_min of minor sector in which points in cycle connected to current point
				compute max_radius in sector measured at centroid
				place point at k * radius * [cos(theta) sin(theta)] for some k
		else:
			place outside cycle
	for every remaining tree:
		place on concave side
repeat while entangled
repeat for every new point
        """

    def coords_as_list(self):
        return [self.coords[i].tolist() for i in range(self.N)]


MAP = Map(MAP_DATA)
