import heapq
import math
import util


@util.timeit
def astar_xd_inner(graph, start: str, goal: str, time: int, heuristic_fn, line_change_value=False):
    goal_node = graph[goal]
    goal_lines = set([x.line for x in goal_node["next_stop"]])
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
        next_idx = came_from[current][5] + 1 if came_from[current] else None

        filtered_stops = [n for n in graph[current]["next_stop"] if n.departure >= current_cost + time]
        filtered_stops_line = [n for n in filtered_stops if n.line in goal_lines]

        if filtered_stops_line:
            filtered_stops = filtered_stops_line

        for neighbor in filtered_stops:
            if neighbor.name in extended:
                continue
            new_cost = neighbor.arrival - time

            if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name] or next_idx == neighbor.idx:
                cost_so_far[neighbor.name] = new_cost
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name, neighbor.idx
                priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name], came_from[current], neighbor, goal_lines)
                heapq.heappush(front, (priority, neighbor.name))

    return came_from, cost_so_far[goal]

@util.print_results_astar
def astar_xd(graph, start: str, goal: str, time: str, heuristic_fn):
    time = util.convert_to_seconds(time)
    line_change_condition = heuristic_fn.__name__ == 'line_change'

    came_from, total_cost = astar_xd_inner(graph, start, goal, time, heuristic_fn, line_change_condition)

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

def haversine_distance(goal, current, came_from_current, neighbor):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    return util.haversine_distance(current_cords, end_cords) * 250


def line_change(goal, current, came_from_current, neighbor, goal_lines):
    current_cords = goal["start_pos"]
    end_cords = current["start_pos"]
    current_line = came_from_current[1] if came_from_current else None
    is_line_changed = 0 if current_line == neighbor.line else 900
    is_goal_line = 0 if neighbor.line in goal_lines else 900
    return 2806 - len(current) + is_goal_line
