import numpy as np
import os
from .constants import (
    BLACK_TICKET,
    BUS_TICKET,
    TAXI_TICKET,
    TICKET_TYPES,
    UNDERGROUND_TICKET,
)
from .ForceDirectedRenderer import force_directed_graph
from .mapdata import MAP_DATA
from .station import Station


class Map:
    """
    Map of the game board.
    Represented as a four layer graph network, with Station objects comprising nodes.
    """

    def __init__(self, map_data: list[list[list[int]]]) -> None:
        """
        Initialize the map.
        Currently using radial generation.
        """
        print("building map...")
        self.N = len(map_data)
        self.map_data = map_data
        self.stations: list[Station] = []
        self.coords: list[tuple[float, float]] = [[x, y] for x, y in zip(*[iter(map(float,open(os.path.dirname(os.path.abspath(__file__))+"/Coordinates.txt","r").read().split(',')))]*2)]
        self.limits = {"min": np.array((0, 0)), "max": np.array((0, 0))}
        self.adjacency_matrix = np.zeros((self.N, self.N))

        self.sub_graphs: dict[str, set[int]] = {
            TAXI_TICKET: set(),
            BUS_TICKET: set(),
            UNDERGROUND_TICKET: set(),
            BLACK_TICKET: set(),
        }

        for i in range(self.N):
            station = Station(i)
            for edge_type in range(len(map_data[i])):
                for j in range(len(map_data[i][edge_type])):
                    neighbour = map_data[i][edge_type][j] - 1
                    station.addNeighbour(TICKET_TYPES[edge_type], neighbour)
                    self.sub_graphs[TICKET_TYPES[edge_type]].add(neighbour)

                    if neighbour >= self.N:
                        continue
                    self.adjacency_matrix[i, neighbour] = 1
            self.stations.append(station)

        print("initialized map with", self.N, "stations.\ngenerating coordinates...")
        #self.coords = {i:p for i, p in enumerate(force_directed_graph(self.N, self.adjacency_matrix))}
        # self.generate_coordinates_radial()
        # self.normalize_coordinates()
        self.compute_limits()
        print(
            f"map generated with dimensions {self.limits['max'][0] - self.limits['min'][0]}x{self.limits['max'][1] - self.limits['min'][1]}"
        )
        print(f"coordinates normalized to {self.get_scale()}")
        # print(f"coordinates: {self.coords}")

    def compute_limits(self):
        """
        Find the limits of the map.
        """
        self.limits["min"] = np.array([np.inf, np.inf])
        self.limits["max"] = np.array([-np.inf, -np.inf])
        for c in self.coords:
            self.limits["min"] = np.minimum(self.limits["min"], c)
            self.limits["max"] = np.maximum(self.limits["max"], c)

    def generate_board_rectangular(self, shape):
        """
        Grid of coordinates, with the origin at the top left corner.
        """

        size = np.product(shape)
        board = np.zeros(size, dtype=int)
        i = np.sort(np.random.choice(np.arange(size), self.N, replace=False))
        board[i] = np.arange(1, self.N + 1)
        return board.reshape(shape)

    @staticmethod
    def einsum_sqrt(a: np.ndarray) -> np.ndarray:
        return np.sqrt(np.einsum("ij,ij->i", a, a))

    def get_gradient(self, coords: np.ndarray):
        s = np.array(list(self.coords.values())) - coords
        d: np.ndarray = np.linalg.norm(s, axis=1).reshape(-1, 1)
        grad = s / (d**2)
        return grad.sum(axis=0), np.min(d)

    def get_scale(self):
        """
        Get the scale of the map.
        """
        return np.linalg.norm(self.limits["max"] - self.limits["min"])

    def generate_coordinates_radial(self):
        """
        ### Radial Coordinate Generation

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

                alpha = 5
                phi = np.random.rand() * 2 * np.pi

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
                        scale = self.get_scale()
                        # print(
                        #     f"{station.location} {station.coords} {neighbour} {computed_cooordinates}: {grad}, {d}, {scale}"
                        # )

                        while d < 1:
                            # print(f"* {neighbour} {computed_cooordinates} {d} {grad}")
                            computed_cooordinates = computed_cooordinates - alpha * grad
                            grad, d = self.get_gradient(computed_cooordinates)

                        self.coords[neighbour] = self.stations[
                            neighbour
                        ].coords = computed_cooordinates

                        self.compute_limits()
                        q.append(self.stations[neighbour])
                # self.normalize_coordinates()

        print("\33[2K[BFS] done.")

        # return self.coords_as_list()

    def normalize_coordinates(self):
        """
        ### Normalize Coordinates

        This function normalizes the coordinates of the stations on the map.
        """
        self.coords = {
            i: (c - self.limits["min"]) / self.get_scale()
            for i, c in self.coords.items()
        }

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
                    # TODO gen bus coords

        # 3. place taxi using bus

        print("\33[2K[BFS bus] done.")
        self.compute_limits()

    def unentangled(self):
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
        raise NotImplementedError()

    # def to_list(self):
    #     """
    #     return coordinates in a serializable format
    #     """
    #     return [c.tolist() for c in self.coords.values()]

    def to_dot(self):
        """
        BFS to generate dot file.
        """

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
        print("\33[2K[DOT taxi] done.")
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
        print("\33[2K[DOT bus] done.")
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
        print("\33[2K[DOT underground] done.")
        r += "}\n}"
        return r


MAP = Map(MAP_DATA)
