from turtle import undo
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
    Represented as a four layer graph network, with Station objects comprising nodes.
    """

    def __init__(self, map_data: list[list[list[int]]] = []) -> None:
        print("building map...")
        self.N = len(map_data)
        self.map_data = map_data
        self.stations: list[Station] = []
        self.coords: dict[int, np.ndarray] = dict()
        self.limits = {"min": [0, 0], "max": [0, 0]}

        self.sub_graphs: dict[str, set[int]] = {
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
        self.generate()
        print(f"limits: {self.limits}\ncoordinates: {self.coords}")

    def generate_limits(self):
        for c in self.coords.values():
            if c[0] < self.limits["min"][0]:
                self.limits["min"][0] = c[0]
            if c[1] < self.limits["min"][1]:
                self.limits["min"][1] = c[1]
            if c[0] > self.limits["max"][0]:
                self.limits["max"][0] = c[0]
            if c[1] > self.limits["max"][1]:
                self.limits["max"][1] = c[1]

    def generate_board_rectangular(self, shape):
        size = np.product(shape)
        board = np.zeros(size, dtype=int)
        i = np.sort(np.random.choice(np.arange(size), self.N, replace=False))
        board[i] = np.arange(1, 201)
        return board.reshape(shape)

    def get_gradient(self, coords):
        grad = np.array([0, 0], dtype=float)
        m = 3
        for c in self.coords.values():
            d = np.linalg.norm(c - coords)
            grad += (c - coords) / (d ** 2)
            m = min(m, d)
        # grad -= coords / (np.linalg.norm(coords))
        return grad, m

    def generate_coordinates_radial(self):
        """
        ### Radial Coordinate Generation
        Romir K.

        This algorithm generates a set of coordinates for the stations on the map.
        """

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
            print(
                f"[BFS] [{progress * '=' + (10 - progress) * ' '}] {len(q)} nodes queued",
                end="\r",
            )
            station = q.pop(0)
            visited[station.location] = True

            for ticket_type, neighbours in station.neighbours.items():

                phi = np.random.rand() * 2 * np.pi
                alpha = 1.1

                for i, neighbour in enumerate(neighbours):
                    if neighbour < self.N and not visited[neighbour]:

                        theta = i * 2 * np.pi / len(neighbours)
                        computed_cooordinates = np.array(
                            (
                                self.coords[station.location][0]
                                + multipliers[ticket_type] * np.cos(theta + phi),
                                self.coords[station.location][1]
                                + multipliers[ticket_type] * np.sin(theta + phi),
                            )
                        )

                        if neighbour in self.coords:
                            computed_cooordinates = (
                                computed_cooordinates + self.coords[neighbour]
                            ) / 2

                        grad, d = self.get_gradient(computed_cooordinates)
                        # print(
                        #     f"{station.location} {station.coords} {neighbour} {computed_cooordinates}: {grad}, {d}"
                        # )

                        while d < 2:
                            # print(f"* {neighbour} {computed_cooordinates} {d} {grad}")
                            computed_cooordinates = computed_cooordinates - alpha * grad
                            grad, d = self.get_gradient(computed_cooordinates)

                        self.coords[neighbour] = self.stations[
                            neighbour
                        ].coords = computed_cooordinates

                        if computed_cooordinates[0] < self.limits["min"][0]:
                            self.limits["min"][0] = computed_cooordinates[0]
                        if computed_cooordinates[1] < self.limits["min"][1]:
                            self.limits["min"][1] = computed_cooordinates[1]
                        if computed_cooordinates[0] > self.limits["max"][0]:
                            self.limits["max"][0] = computed_cooordinates[0]
                        if computed_cooordinates[1] > self.limits["max"][1]:
                            self.limits["max"][1] = computed_cooordinates[1]

                        q.append(self.stations[neighbour])

        print("[BFS] done.                                  ")
        # return self.coords_as_list()

    def generate(self, xmax=500, ymax=500):
        """
        Procedural Coordinate Generation
        """
        # 1. place underground
        underground_stations = list(self.sub_graphs[UNDERGROUND_TICKET])
        n_u = len(underground_stations)
        # d = (xmax * ymax / n_u ) ** 0.5
        for i in range(n_u):
            x = np.random.rand() * xmax
            y = np.random.rand() * ymax
            self.coords[underground_stations[i]] = np.array((x, y))

        print(f"placed {n_u} underground stations")

        # 2. place bus using underground
        bus_stations = list(self.sub_graphs[BUS_TICKET])
        n_b = len(bus_stations)
        visited = np.zeros(n_b, dtype=bool)
        q = list(self.sub_graphs[UNDERGROUND_TICKET])
        r = (xmax * ymax / n_b) ** 0.5
        while q:
            progress = int(np.count_nonzero(visited) / n_b * 10)
            print(
                f"[BFS bus] [{progress * '=' + (10 - progress) * ' '}] {len(q)} nodes queued",
                end="\r",
            )
            idx = q.pop(0)
            if idx >= self.N:
                # print(f"{idx} not in stations")
                continue
            station = self.stations[idx]
            visited[bus_stations.index(station.location)] = True
            for neighbour in station.neighbours[BUS_TICKET]:
                # neighbour = self.stations[neighbour]
                if not visited[bus_stations.index(neighbour)]:
                    q.append(neighbour)
                    if neighbour in self.coords:
                        continue
        print("[BFS bus] done.                                  ")
        self.generate_limits()

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
        return [c.tolist() for c in self.coords.values()]
    
    def to_dot(self):
        r = "graph {\nsubgraph taxi {\n"
        visited = np.zeros(self.N, dtype=bool)
        q = [self.stations[0]]
        while q:
            progress = int(np.count_nonzero(visited) / self.N * 10)
            print(
                f"[DOT taxi] [{progress * '=' + (10 - progress) * ' '}] {len(q)} nodes queued",
                end="\r",
            )
            station = q.pop(0)
            visited[station.location] = True
            for neighbour in station.neighbours[TAXI_TICKET]:
                if neighbour < self.N and not visited[neighbour]:
                    r += f"{station.location} -- {neighbour}\n"
                    q.append(self.stations[neighbour])
        print("[DOT taxi] done.                                  ")
        r += "}\nsubgraph bus {\n"
        visited = np.zeros(self.N, dtype=bool)
        q = [self.stations[0]]
        while q:
            progress = int(np.count_nonzero(visited) / self.N * 10)
            print(
                f"[DOT bus] [{progress * '=' + (10 - progress) * ' '}] {len(q)} nodes queued",
                end="\r",
            )
            station = q.pop(0)
            visited[station.location] = True
            for neighbour in station.neighbours[BUS_TICKET]:
                if neighbour < self.N and not visited[neighbour]:
                    r += f"{station.location} -- {neighbour}\n"
                    q.append(self.stations[neighbour])
        print("[DOT bus] done.                                  ")
        r += "}\nsubgraph underground {\n"
        visited = np.zeros(self.N, dtype=bool)
        q = [self.stations[0]]
        while q:
            progress = int(np.count_nonzero(visited) / self.N * 10)
            print(
                f"[DOT underground] [{progress * '=' + (10 - progress) * ' '}] {len(q)} nodes queued",
                end="\r",
            )
            station = q.pop(0)
            visited[station.location] = True
            for neighbour in station.neighbours[UNDERGROUND_TICKET]:
                if neighbour < self.N and not visited[neighbour]:
                    r += f"{station.location} -- {neighbour}\n"
                    q.append(self.stations[neighbour])
        print("[DOT underground] done.                                  ")
        r += "}\n}"
        return r



MAP = Map(MAP_DATA)
