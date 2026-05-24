from itertools import permutations


def solve_route(distance_matrix):
    """
    Simple but SAFE TSP solver (works for assignment + deployment)
    Returns best route based on minimum distance
    """

    nodes = list(distance_matrix.keys())

    if len(nodes) < 2:
        return nodes

    best_route = None
    best_cost = float("inf")

    # try all permutations (safe for small assignment datasets)
    for perm in permutations(nodes):

        cost = 0
        valid = True

        for i in range(len(perm) - 1):
            a, b = perm[i], perm[i + 1]

            if b not in distance_matrix[a]:
                valid = False
                break

            cost += distance_matrix[a][b]

        if valid and cost < best_cost:
            best_cost = cost
            best_route = perm

    return list(best_route) if best_route else nodes
