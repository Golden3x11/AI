import heapq
import math
import util


@util.timeit
def astar_inner(graph, start: str, goal: str, time: int, heuristic_fn, line_change_value=False):
    goal_node = graph[goal]
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    extended = set()

    while front:
        _, current = heapq.heappop(front)
        extended.add(current)
        if current == goal:
            break
        current_cost = cost_so_far[current]
        next_idx = came_from[current][4] + 1 if came_from[current] else None
        filtered_stops = (n for n in graph[current]["next_stop"] if n.departure >= current_cost + time)

        for neighbor in filtered_stops:
            if neighbor.name in extended:
                continue
            new_cost = neighbor.arrival - time
            if line_change_value:
                condition = lambda: (next_idx == neighbor.idx)
            else:
                condition = lambda: (new_cost <= cost_so_far[neighbor.name] and next_idx == neighbor.idx)

            if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name] or condition():
                cost_so_far[neighbor.name] = new_cost
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.idx
                priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name], came_from[current], neighbor)
                heapq.heappush(front, (priority, neighbor.name))

    return came_from, cost_so_far[goal]


@util.print_results_astar
def astar(graph, start: str, goal: str, time: str, heuristic_fn):
    time = util.convert_to_seconds(time)
    line_change_condition = heuristic_fn.__name__ == 'line_change'

    came_from, total_cost = astar_inner(graph, start, goal, time, heuristic_fn, line_change_condition)

    path = [goal]
    current = came_from[goal]
    while current[0] != start:
        path.append((current[0], current[1],
                     util.convert_to_time_string(current[2]),
                     util.convert_to_time_string(current[3])))
        current = came_from[current[0]]

    path.append((current[0], current[1],
                 util.convert_to_time_string(current[2]),
                 util.convert_to_time_string(current[3])))

    path.reverse()
    return total_cost, path


def manhattan_distance(goal, current):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    return sum([abs(x1 - x2) for x1, x2 in zip(current_cords, end_cords)]) * 69000


def haversine_distance(goal, current, came_from_current, neighbor):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    return util.haversine_distance(current_cords, end_cords) * 250


def line_change(goal, current, came_from_current, neighbor):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    current_line = came_from_current[1] if came_from_current else None
    is_line_changed = 0 if current_line == neighbor.line else 1500
    return util.haversine_distance(current_cords, end_cords) * 250 + is_line_changed
