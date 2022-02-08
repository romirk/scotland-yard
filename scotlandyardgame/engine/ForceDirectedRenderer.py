"""
Force Directed Graph Drawing

Implementation of the force directed graph drawing algorithm.
(C) 2022 Romir Kulshrestha (https://github.com/romirk)

You should have received a copy of the MIT license with this file.
If not, see https://opensource.org/licenses/MIT.
"""
# This thing is so legit I needed to make it its own file

import numpy as np
import numpy.linalg as la


def combinations(n):
    return np.transpose(np.triu_indices(n, 1))


def compute_distances(p: np.ndarray):
    """
    Computes the distance matrix between all vertices.
    """
    N = p.shape[0]
    c = np.zeros((N, N))
    for i, j in combinations(N):
        c[i, j] = c[j, i] = la.norm(p[i] - p[j])
    return c


def get_field(p: np.ndarray):
    N = p.shape[0]
    c = np.zeros((N, N))
    for i, j in combinations(N):
        c[i, j] = (p[i] - p[j]) / la.norm(p[i] - p[j])
        c[j, i] = -c[i, j]
    return c


def compute_attraction(
    p: np.ndarray, field: np.ndarray, c: np.ndarray, adjacency_matrix: np.ndarray
) -> np.ndarray:
    """
    Computes the attraction force acting on each vertex, if they are connected by an edge.
    """
    return np.log(c * adjacency_matrix) * field


def compute_repulsion(p: np.ndarray, field: np.ndarray, c: np.ndarray):
    """
    Computes the repulsion force acting on each vertex according to the inverse square law.
    """
    return field / (c**2)


def force_directed_graph(
    n: int,
    adjacency_matrix: np.ndarray,
    xmax=500,
    ymax=500,
    repulsion_constant=0.89875,
    attraction_constant=0.66743,
    iterations=100,
) -> np.ndarray:
    """
    Computes the force directed graph layout for the given graph.
    Returns an ndarray representing the cartesian coordinates of the nodes.

    For fun, the attraction and repulsion constants default to the universal gravitational constant
    and the Coulomb constant respectively (although in arbitrary scale).
    """

    # From https://stackoverflow.com/a/23598527/5224022:

    # > The idea is to consider vertices to naturally repel each other, but edges to draw them
    # > together. Both forces (repulsion and attraction) should be functions of distance between
    # > vertices, and act directly towards (or away from) the relevant vertex. Magnitudes like
    # > (1/r^2) for a repulsive force and ln(r) for an attractive force is good. Also consider
    # > some repulsive forces applied at boundaries to stop separate connected components flying
    # > off to infinity.
    # >
    # > That algorithm goes something like:
    # >     - Place all vertices at random points on the plane.
    # >     - Calculate the net forces acting on each vertex.
    # >     - Move each of the vertices by a fraction of the net forces.
    # >     - If no vertex moved more than some tolerance value, draw the graph, else go to 2.

    # The algorithm is a bit more complicated than that, but it's still a bit of a brute force.
    # It's not a particularly good algorithm, but it's a good one.

    # Step 1: Place all vertices at random points on the plane.
    # The primary index of p corresponds to the specific station on the map represented by the
    # vertex.
    p = np.random.rand(n, 2) * np.array((xmax, ymax))

    i = 0
    while i < iterations:
        # Step 2: Calculate the net forces acting on each vertex.
        # This is the sum of the attractive and repulsive forces acting on each vertex.
        # The attractive forces are calculated by the distance between the vertices and are independent of edges.
        # The repulsive forces are calculated by the distance between the vertices squared.

        # populate the distance matrix with distances between each station.
        c = compute_distances(p)

        # compute the directional field
        field = get_field(p)

        repulsive_forces = compute_repulsion(p, field, c) * repulsion_constant
        attractive_forces = (
            compute_attraction(p, field, c, adjacency_matrix) * attraction_constant
        )

        # apply the forces to the vertices.
        c = c + attractive_forces + repulsive_forces
