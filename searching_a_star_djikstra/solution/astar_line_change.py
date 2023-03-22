import heapq

import util


@util.timeit
def astar_line_inner(graph, start: str, goal: str, time: int, heuristic_fn):
    goal_lines_dict = {x.line: True for x in graph[goal]["next_stop"]}
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: (0, 0, 0)}
    extended = set()

    while front:
        _, current = heapq.heappop(front)
        if current in extended:
            continue
        extended.add(current)
        if current == goal:
            break
        current_cost = cost_so_far[current][0]
        current_time = cost_so_far[current][1]
        line = came_from[current][1] if came_from[current] else None

        filtered_stops = [n for n in graph[current]["next_stop"] if n.departure >= current_time + time and n.name not in extended]

        for neighbor in filtered_stops:
            new_cost = (0 if line == neighbor.line else 250) + current_cost
            new_time = neighbor.arrival - time
            priority = new_cost + new_time + heuristic_fn(graph[neighbor.name], neighbor, goal_lines_dict)

            if neighbor.name not in cost_so_far or priority < cost_so_far[neighbor.name][2] or priority == cost_so_far[neighbor.name][2] and new_time < cost_so_far[neighbor.name][1]:
                cost_so_far[neighbor.name] = new_cost, new_time, priority
                came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name
                heapq.heappush(front, (priority, neighbor.name))
    return came_from, cost_so_far[goal][1]

@util.print_results_astar
def astar_line(graph, start: str, goal: str, time: str, heuristic_fn):
    time = util.convert_to_seconds(time)

    came_from, total_cost = astar_line_inner(graph, start, goal, time, heuristic_fn)

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


def line_change(neighbor_node, neighbor, goal_lines_dict):
    is_goal_line = 0 if neighbor.line in goal_lines_dict else 900
    return (2806 - len(neighbor_node["next_stop"])) /10 + is_goal_line