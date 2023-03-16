import heapq
import math
import util


@util.timeit
def astar_inner(graph, start: str, goal: str, time: int, heuristic_fn):
    goal_node = graph[goal]
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while front:
        _, current = heapq.heappop(front)

        if current == goal:
            break
        current_cost = cost_so_far[current]
        filtered_stops = (n for n in graph[current]["next_stop"] if n.departure >= current_cost + time)

        for neighbor in filtered_stops:
            new_cost = neighbor.arrival - time
            if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name]:
                cost_so_far[neighbor.name] = new_cost
                priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name])
                heapq.heappush(front, (priority, neighbor.name))
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival

    return came_from, cost_so_far[goal]


def astar(graph, start: str, goal: str, time: str, heuristic_fn):
    time = util.convert_to_seconds(time)
    came_from, total_cost = astar_inner(graph, start, goal, time, heuristic_fn)

    path = [goal]
    current = came_from[goal][0]
    while current != start:
        current = came_from[current]
        path.append((current[0], current[1],
                     util.convert_to_time_string(current[2]),
                     util.convert_to_time_string(current[3])))
        current = current[0]

    path.reverse()
    return path, util.convert_to_time_string(total_cost)


def manhattan_distance(a, b):
    current_cords = a["start_pos"]
    end_cords = b["start_pos"]
    return sum([abs(x1 - x2) for x1, x2 in zip(current_cords, end_cords)]) * 100


def euclidean_distance(a, b):
    current_cords = a["start_pos"]
    end_cords = b["start_pos"]
    return math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(current_cords, end_cords)])) * 100


def towncenter_distance(a, b):
    return euclidean_distance(a, (0, 0, 0, 0, 0, 0, 0)) + euclidean_distance((0, 0, 0, 0, 0, 0, 0), b)


def unidimensional_distance(a, b):
    return max([abs(x - y) for x, y in zip(a, b)])


def cosine_distance(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))
    return 1 - (dot_product / (magnitude_a * magnitude_b))


def chebyshev_distance(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


if __name__ == '__main__':
    graph = {
        (0, 0, 0, 0, 0, 0, 0): [(1, 1, 1, 1, 1, 1, 1), (1, 2, 3, 4, 5, 6, 7), (4, 5, 6, 7, 8, 9, 10),
                                (5, 6, 7, 8, 6, 5, 1)],
        (1, 2, 3, 4, 5, 6, 7): [(2, 3, 4, 5, 6, 7, 8), (1, 1, 1, 1, 1, 1, 1), (5, 2, 1, 4, 1, 3, 1)],
        (2, 3, 4, 5, 6, 7, 8): [(3, 4, 5, 6, 7, 8, 9), (2, 4, 2, 1, 4, 1, 8), (1, 2, 3, 4, 5, 6, 7),
                                (5, 6, 7, 8, 6, 5, 1), (6, 6, 10, 2, 2, 5, 10), (9, 3, 2, 7, 0, 0, 1),
                                (9, 9, 2, 0, 2, 1, 9)],
        (3, 4, 5, 6, 7, 8, 9): [(4, 5, 6, 7, 8, 9, 10)],
        (4, 5, 6, 7, 8, 9, 10): [],
        (1, 1, 1, 1, 1, 1, 1): [(2, 2, 2, 2, 2, 2, 2), (5, 2, 1, 4, 1, 3, 1), (6, 6, 10, 2, 2, 5, 10),
                                (10, 10, 10, 10, 10, 10, 10)],
        (2, 2, 2, 2, 2, 2, 2): [],
        (5, 2, 1, 4, 1, 3, 1): [(2, 2, 2, 2, 2, 2, 2), (2, 0, 2, 0, 2, 0, 2), (2, 4, 2, 1, 4, 1, 8),
                                (3, 4, 5, 6, 7, 8, 9), (9, 9, 2, 0, 2, 1, 9)],
        (2, 0, 2, 0, 2, 0, 2): [],
        (2, 2, 2, 2, 2, 2, 2): [(2, 3, 4, 5, 6, 7, 8), (2, 2, 2, 2, 2, 2, 2), (4, 5, 6, 7, 8, 9, 10),
                                (5, 6, 7, 8, 6, 5, 1), (10, 10, 10, 10, 10, 10, 10)],
        (3, 3, 2, 0, 1, 0, 1): [(1, 2, 3, 4, 5, 6, 7), (2, 2, 2, 2, 2, 2, 2), (2, 3, 4, 5, 6, 7, 8),
                                (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2), (6, 6, 10, 2, 2, 5, 10),
                                (2, 2, 2, 2, 2, 2, 2)],
        (5, 6, 7, 8, 6, 5, 1): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)],
        (6, 6, 10, 2, 2, 5, 10): [(2, 0, 2, 0, 2, 0, 2), (1, 1, 1, 1, 1, 1, 1)],
        (2, 4, 2, 1, 4, 1, 8): [(1, 2, 3, 4, 5, 6, 7), (5, 2, 1, 4, 1, 3, 1), (2, 0, 2, 0, 2, 0, 2)],
        (9, 3, 2, 7, 0, 0, 1): [(5, 2, 1, 4, 1, 3, 1), (10, 10, 10, 10, 10, 10, 10)],
        (9, 9, 2, 0, 2, 1, 9): [(2, 0, 2, 0, 2, 0, 2), (10, 10, 10, 10, 10, 10, 10)],
        (10, 10, 10, 10, 10, 10, 10): [(2, 0, 2, 0, 2, 0, 2), (3, 4, 5, 6, 7, 8, 9)]
    }

    start = (1, 2, 3, 4, 5, 6, 7)
    goal = (10, 10, 10, 10, 10, 10, 10)

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: manhattan_distance(a, b))
    print(f"Path using Manhattan distance heuristic: {path}")
    print(f"Cost using Manhattan distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: euclidean_distance(a, b))
    print(f"Path using Euclid's distance heuristic: {path}")
    print(f"Cost using Euclid's distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: towncenter_distance(a, b))
    print(f"Path using Towncenter distance heuristic: {path}")
    print(f"Cost using Towncenter distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: unidimensional_distance(a, b))
    print(f"Path using unidimensional distance heuristic: {path}")
    print(f"Cost using unidimensional distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: cosine_distance(a, b))
    print(f"Path using cosine distance heuristic: {path}")
    print(f"Cost using cosine distance heuristic: {cost}")

    path, cost = astar(start, goal, lambda node: graph[node], lambda a, b: chebyshev_distance(a, b))
    print(f"Path using Chebyshev distance heuristic: {path}")
    print(f"Cost using Chebyshev distance heuristic: {cost}")
