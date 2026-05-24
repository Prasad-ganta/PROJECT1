from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)


# ==========================================
# SOLVE ROUTE USING OR-TOOLS
# ==========================================

def solve_route(distance_matrix):

    locations = list(distance_matrix.keys())

    num_locations = len(locations)

    # CREATE ROUTING INDEX MANAGER

    manager = pywrapcp.RoutingIndexManager(
        num_locations,
        1,
        0
    )

    # CREATE ROUTING MODEL

    routing = pywrapcp.RoutingModel(manager)

    # DISTANCE CALLBACK

    def distance_callback(from_index, to_index):

        from_node = manager.IndexToNode(from_index)

        to_node = manager.IndexToNode(to_index)

        from_location = locations[from_node]

        to_location = locations[to_node]

        return int(
            distance_matrix[from_location][to_location]
        )

    transit_callback_index = (
        routing.RegisterTransitCallback(
            distance_callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    # SEARCH PARAMETERS

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy
        .PATH_CHEAPEST_ARC
    )

    # SOLVE

    solution = routing.SolveWithParameters(
        search_parameters
    )

    # IF NO SOLUTION

    if solution is None:

        return locations

    # EXTRACT ROUTE

    index = routing.Start(0)

    optimized_route = []

    while not routing.IsEnd(index):

        node_index = manager.IndexToNode(index)

        optimized_route.append(
            locations[node_index]
        )

        index = solution.Value(
            routing.NextVar(index)
        )

    return optimized_route