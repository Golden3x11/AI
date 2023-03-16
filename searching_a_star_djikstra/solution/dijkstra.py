import heapq
import util

@util.timeit
def dijkstra(graph_dict, start, goal, time):
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = time
    pq = [(time, start)]
    prev_nodes = {node: None for node in graph_dict}

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        line = prev_nodes[curr_node][1] if prev_nodes[curr_node] else None
        if curr_node == goal:
            break
        if curr_dist > distances[curr_node]:
            continue

        filtered_stops = (n for n in graph_dict[curr_node]["next_stop"] if n.departure >= curr_dist)

        for next_stop in filtered_stops:
            new_dist = next_stop.arrival
            neighbor = next_stop.name
            if new_dist < distances[neighbor] or (new_dist <= distances[neighbor] and line == next_stop.line and next_stop.name != curr_node):
                distances[neighbor] = new_dist
                prev_nodes[neighbor] = (curr_node, next_stop.line, next_stop.departure, next_stop.arrival)
                heapq.heappush(pq, (new_dist, neighbor))


    return distances, prev_nodes


def shortest_path(graph, start, goal, start_time):
    start_time = util.convert_to_seconds(start_time)
    distances, previous_nodes = dijkstra(graph, start, goal, start_time)
    path = [goal]
    current_node = previous_nodes[goal]
    while current_node is not None:
        path.append((current_node[0], current_node[1],
                     util.convert_to_time_string(current_node[2]),
                     util.convert_to_time_string(current_node[3])))
        current_node = previous_nodes[current_node[0]]
    path.reverse()
    return util.convert_to_time_string(distances[goal] - start_time), path
