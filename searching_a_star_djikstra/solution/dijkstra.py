import heapq
import util

@util.timeit
def dijkstra(graph_dict, start, goal, time):
    distances = {node: float('inf') for node in graph_dict}
    distances[start] = 0
    pq = [(0, start)]
    prev_nodes = {node: None for node in graph_dict}

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        next_idx = prev_nodes[curr_node][5] + 1 if prev_nodes[curr_node] else None
        if curr_dist > distances[curr_node]:
            continue

        filtered_stops = (n for n in graph_dict[curr_node]["next_stop"] if n.departure >= curr_dist + time)

        for neighbor in filtered_stops:
            new_dist = neighbor.arrival - time
            if new_dist < distances[neighbor.name] or (new_dist <= distances[neighbor.name] and next_idx == neighbor.idx):
                distances[neighbor.name] = new_dist
                prev_nodes[neighbor.name] = (curr_node, neighbor.line, neighbor.departure, neighbor.arrival, neighbor.name, neighbor.idx)
                heapq.heappush(pq, (new_dist, neighbor.name))


    return distances, prev_nodes

@util.print_results_djikstra
def shortest_path(graph, start, goal, start_time):
    start_time = util.convert_to_seconds(start_time)
    distances, previous_nodes = dijkstra(graph, start, goal, start_time)
    path = []
    current_node = previous_nodes[goal]
    while current_node is not None:
        path.append((current_node[0], current_node[1],
                     util.convert_to_time_string(current_node[2]),
                     util.convert_to_time_string(current_node[3]), current_node[4]))
        current_node = previous_nodes[current_node[0]]
    path.reverse()
    return (distances[goal]), path
