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
    f = np.zeros((N, N, 2))
    for i, j in combinations(N):
        f[i, j] = (p[i] - p[j]) / la.norm(p[i] - p[j])
        f[j, i] = -f[i, j]
    return f


def compute_attraction(
    field: np.ndarray, c: np.ndarray, adjacency_matrix: np.ndarray
) -> np.ndarray:
    """
    Computes the attraction force acting on each vertex, if they are connected by an edge.
    """
    l = np.log(c)
    l[np.diag_indices(c.shape[0])] = 0
    l *= adjacency_matrix
    a = np.repeat(l[:, :, np.newaxis], 2, axis=2) * field
    # print(f"a: {a[0]}")
    return a


def compute_repulsion(field: np.ndarray, c: np.ndarray):
    """
    Computes the repulsion force acting on each vertex according to the inverse square law.
    """
    r = -np.divide(field, np.repeat(c[:, :, np.newaxis], 2, axis=2))
    r[np.diag_indices(c.shape[0])] = np.array((0, 0))
    # print(f"r: {r[0]}")
    return r


def apply_forces(p: np.ndarray, f: np.ndarray):
    """
    Applies the forces to the vertices.
    """
    return p + np.add.reduce(f, axis=1)


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
    # print(p[0])
    # print(adjacency_matrix[0])

    i = 0
    while i < iterations:
        progress = int((i / iterations) * 10)
        print(
            f"[FDG] [{progress * '=' + (10 - progress) * ' '}]",
            end="\r",
        )
        # Step 2: Calculate the net forces acting on each vertex.
        # This is the sum of the attractive and repulsive forces acting on each vertex.
        # The attractive forces are calculated by the distance between the vertices and are independent of edges.
        # The repulsive forces are calculated by the distance between the vertices squared.

        # populate the distance matrix with distances between each station.
        c = compute_distances(p)

        # compute the directional field
        field = get_field(p)

        repulsive_forces = compute_repulsion(field, c) * repulsion_constant
        attractive_forces = (
            compute_attraction(field, c, adjacency_matrix) * attraction_constant
        )
        net_forces = attractive_forces + repulsive_forces
        # print(f"net_forces: {net_forces[0]}")
        # apply the forces to the vertices.
        p = apply_forces(p, net_forces)
        # print(p[0], p.shape)
        i += 1
    return p
