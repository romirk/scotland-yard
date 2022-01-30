import numpy as np
from scotlandyardgame.engine.constants import (
    BLACK_TICKET,
    BUS_TICKET,
    TAXI_TICKET,
    UNDERGROUND_TICKET,
)

from .map import Map
from heapq import heappop, heappush


def generate_board_bfs(map: Map):
    stations = map.stations.copy()
    q = [(1, stations[0])]
    stations[0] = None
    type_multipliers = {
        TAXI_TICKET: 2,
        BUS_TICKET: 3,
        UNDERGROUND_TICKET: 5,
        BLACK_TICKET: 7,
    }
    r = []
    i = 1
    while q:
        d, station = heappop(q)
        print(f"[BFS] {i} of {len(stations)} at {d}", end="\r")
        r.append(station.location)
        for ticket_type, neighbours in station.neighbours.items():
            for neighbour in neighbours:
                if neighbour < map.N and stations[neighbour] is not None:
                    heappush(
                        q,
                        (d * (type_multipliers[ticket_type]), stations[neighbour]),
                    )
                    stations[neighbour] = None
        i += 1
    print("[BFS] done.            ")
    return r
