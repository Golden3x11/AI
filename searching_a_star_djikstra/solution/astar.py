import heapq
import math

import util


@util.timeit
def astar_inner(graph, start: str, goal: str, time: int, heuristic_fn):
    goal_node = graph[goal]
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    extended = set()

    while front:
        _, current = heapq.heappop(front)
        if current == goal:
            break

        if current in extended:
            continue
        extended.add(current)
        current_cost = cost_so_far[current]

        for neighbor in (n for n in graph[current]["next_stop"] if n.departure >= current_cost + time and n.name not in extended):
            new_cost = neighbor.arrival - time

            if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name]:
                cost_so_far[neighbor.name] = new_cost
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name
                priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name])
                heapq.heappush(front, (priority, neighbor.name))

    return came_from, cost_so_far[goal]


@util.print_results_astar
def astar(graph, start: str, goal: str, time: str, heuristic_fn):
    time = util.convert_to_seconds(time)

    came_from, total_cost = astar_inner(graph, start, goal, time, heuristic_fn)

    path = []
    current = came_from[goal]
    while current[0] != start:
        path.append((current[0], current[1],
                     util.convert_to_time_string(current[2]),
                     util.convert_to_time_string(current[3]), current[4]))
        current = came_from[current[0]]

    path.append((current[0], current[1],
                 util.convert_to_time_string(current[2]),
                 util.convert_to_time_string(current[3]), current[4]))

    path.reverse()
    return total_cost, path

def haversine_distance(goal, current):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    return util.haversine_distance(current_cords, end_cords) * 250

# to equal value to haversine
MANHATTAN_MULTIPLY = 16114
def manhattan_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return sum([abs(x - y) for x, y in zip(a, b)]) * MANHATTAN_MULTIPLY

# to equal value to haversine
EUCLIDEAN_MULTIPLY = 22767
def euclidean_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)])) * EUCLIDEAN_MULTIPLY

# to equal value to haversine
UNIDIMENSIONAL_MULTIPLY = 30876
def unidimensional_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return max([abs(x - y) for x, y in zip(a, b)]) * UNIDIMENSIONAL_MULTIPLY

# to equal value to haversine
COSINE_MULTIPLY = 11002895338
def cosine_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))
    return 1 - (dot_product / (magnitude_a * magnitude_b)) * COSINE_MULTIPLY

# to equal value to haversine
CHEBYSHEV_MULTIPLY = 30876
def chebyshev_distance(a, b):
    a = a["start_pos"]
    b = b["start_pos"]
    return max(abs(x - y) for x, y in zip(a, b)) * CHEBYSHEV_MULTIPLY
