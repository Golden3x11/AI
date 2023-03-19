from dijkstra import shortest_path
from astar import *
from tabu_search import *
from util import Cords, NextStop
import util

import pandas as pd

df = pd.read_csv('exercise/connection_graph_2.csv', dtype={"line": str})

graph = {}

for _, row in df.iterrows():
    start = row["start_stop"]
    end = row["end_stop"]  # station 'Żórawina - Niepodległości (Mostek)' is only end station

    start_pos = Cords(row["start_stop_lat"], row["start_stop_lon"])
    end_pos = Cords(row["end_stop_lat"], row["end_stop_lon"])
    next_stop = NextStop(row[0], row["end_stop"], end_pos, row["line"],
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
    graph[end]["start_pos"].add(end_pos)

util.update_start_pos(graph)

shortest_path(graph, "Lubiatów", "Kątna", "00:00:00")
astar(graph, "Lubiatów", "Kątna", "00:00:00", heuristic_fn=haversine_distance)
astar(graph, "Lubiatów", "Kątna", "00:00:00", heuristic_fn=line_change)

shortest_path(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00")
astar(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=haversine_distance)
astar(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=line_change)

shortest_path(graph, "Żmudzka", "PL. GRUNWALDZKI", "16:00:00")
astar(graph, "Żmudzka", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=haversine_distance)
astar(graph, "Żmudzka", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=line_change)

shortest_path(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00")
astar(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00", heuristic_fn=haversine_distance)
astar(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00", heuristic_fn=line_change)

tabu_search(graph, "Reja", ["PL. GRUNWALDZKI", "ZACHODNIA (Stacja kolejowa)", "DWORZEC NADODRZE", "Żmudzka", "ZOO", "Zakładowa", "Bajana", "Wyszyńskiego"])