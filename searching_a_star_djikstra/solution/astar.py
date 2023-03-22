import heapq
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
        if current in extended:
            continue
        extended.add(current)
        if current == goal:
            break
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

