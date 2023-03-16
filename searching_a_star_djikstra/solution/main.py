from dijkstra import shortest_path
from astar import *
from util import Cords, NextStop
import util

import pandas as pd

df = pd.read_csv('exercise/connection_graph_2.csv', dtype={"line": str})

graph = {}

for _, row in df.iterrows():
    start = row["start_stop"]
    end = row["end_stop"] # station 'Żórawina - Niepodległości (Mostek)' is only end station

    start_pos = Cords(row["start_stop_lat"], row["start_stop_lon"])
    next_stop = NextStop(row["end_stop"], Cords(row["end_stop_lat"], row["end_stop_lon"]), row["line"],
                         util.convert_to_seconds(row["departure_time"]),
                         util.convert_to_seconds(row["arrival_time"]))

    if start not in graph:
        graph[start] = {
            "start_pos": set(),
            "next_stop": []
        }
    if end not in graph:
        graph[end] = {
            "start_pos": set(),
            "next_stop": []
        }

    graph[start]["start_pos"].add(start_pos)
    graph[start]["next_stop"].append(next_stop)

util.update_start_pos(graph)

distance, path = shortest_path(graph, "Lubiatów", "Kątna", "00:00:00")
print("Shortest distance:", distance)
print("Shortest path:", path)

print()

path, cost = astar(graph, "Lubiatów", "Kątna", "00:00:00", lambda a, b: manhattan_distance(a, b))
print(f"Cost using Euclid's distance heuristic: {cost}")
print(f"Path using Euclid's distance heuristic: {path}")

print()


distance, path = shortest_path(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00")
print("Shortest distance:", distance)
print("Shortest path:", path)

print()


path, cost = astar(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00", lambda a, b: manhattan_distance(a, b))
print(f"Cost using Euclid's distance heuristic: {cost}")
print(f"Path using Euclid's distance heuristic: {path}")

print()

distance, path = shortest_path(graph, "Żmudzka", "PL. GRUNWALDZKI", "16:00:00")
print("Shortest distance:", distance)
print("Shortest path:", path)

print()

path, cost = astar(graph, "Żmudzka", "PL. GRUNWALDZKI", "16:00:00", lambda a, b: euclidean_distance(a, b))
print(f"Cost using Euclid's distance heuristic: {cost}")
print(f"Path using Euclid's distance heuristic: {path}")
