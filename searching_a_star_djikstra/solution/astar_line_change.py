# import heapq
# import math
# import util
#
#
# @util.timeit
# def astar_line_change_inner(graph, start: str, goal: str, time: int, heuristic_fn):
#     goal_node = graph[goal]
#     front = [(0, start)]
#     came_from = {start: None}
#     cost_so_far = {start: 0}
#
#     while front:
#         _, current = heapq.heappop(front)
#
#         if current == goal:
#             break
#         current_cost = cost_so_far[current]
#         next_idx = came_from[current][4] + 1 if came_from[current] else None
#         filtered_stops = (n for n in graph[current]["next_stop"] if n.departure >= current_cost + time)
#
#         for neighbor in filtered_stops:
#             new_cost = neighbor.arrival - time
#             if neighbor.name not in cost_so_far or new_cost < cost_so_far[neighbor.name] or next_idx == neighbor.idx:
#                 cost_so_far[neighbor.name] = new_cost
#                 priority = new_cost + heuristic_fn(goal_node, graph[neighbor.name], came_from[current], neighbor)
#
#                 heapq.heappush(front, (priority, neighbor.name))
#                 came_from[neighbor.name] = current, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.idx
#
#     return came_from, cost_so_far[goal]
#
#
# @util.print_results_astar
# def astar_line_change(graph, start: str, goal: str, time: str, heuristic_fn):
#     time = util.convert_to_seconds(time)
#     came_from, total_cost = astar_line_change_inner(graph, start, goal, time, heuristic_fn)
#     path = [goal]
#     current = came_from[goal]
#     while current[0] != start:
#         path.append((current[0], current[1],
#                      util.convert_to_time_string(current[2]),
#                      util.convert_to_time_string(current[3])))
#         current = came_from[current[0]]
#
#     path.append((current[0], current[1],
#                      util.convert_to_time_string(current[2]),
#                      util.convert_to_time_string(current[3])))
#
#     path.reverse()
#     return total_cost, path
#
#
# def line_change(goal, current, came_from_current, neighbor):
#     current_cords = goal["start_pos"]
#     end_cords = current["start_pos"]
#     current = current["next_stop"]
#     current_line = came_from_current[1] if came_from_current else None
#     is_line_changed = 900 if current_line == neighbor.line else 0
#     return (2806 - len(current) + util.haversine_distance(current_cords, end_cords) * 250)/2 + is_line_changed
#
#
