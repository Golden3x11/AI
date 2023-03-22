import pandas as pd

from astar import *
from dijkstra import shortest_path
from searching_a_star_djikstra.solution import astar_line_change
from searching_a_star_djikstra.solution.astar_line_change import astar_line
from tabu_search import *
from util import Cords, NextStop


def load_data():
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
    return graph

def dijkstra(graph, start_stop, end_stop, time):
    shortest_path(graph, start_stop, end_stop, time)
def a_star(graph, start_stop, end_stop, time, optimization):
    if optimization == "p":
        astar_line(graph, start_stop, end_stop, time, heuristic_fn=astar_line_change.line_change)
    elif optimization == "t":
        astar(graph, start_stop, end_stop, time, heuristic_fn=haversine_distance)

if __name__ == '__main__':
    graph = load_data()
    start_stop = "Żmudzka"
    end_stop = "PL. GRUNWALDZKI"
    time = "16:00:00"
    optimization = "p"
    L = ["PL. GRUNWALDZKI", "ZACHODNIA (Stacja kolejowa)", "DWORZEC NADODRZE", "Żmudzka", "ZOO", "Zakładowa", "Bajana",
         "Wyszyńskiego", "Kominiarska", "Kwidzyńska", "Piramowicza", "Rdestowa", "Tęczowa", "Volvo", "Śrubowa"]

    dijkstra(graph, start_stop, end_stop, time)
    a_star(graph, start_stop, end_stop, time, optimization)
    a_star(graph, start_stop, end_stop, time, "t")

    shortest_path(graph, "Lubiatów", "Kątna", "00:00:00")
    astar(graph, "Lubiatów", "Kątna", "00:00:00", heuristic_fn=haversine_distance)
    astar_line(graph, "Lubiatów", "Kątna", "00:00:00", heuristic_fn=astar_line_change.line_change)

    shortest_path(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00")
    astar(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=haversine_distance)
    astar_line(graph, "Sowia", "PL. GRUNWALDZKI", "16:00:00", heuristic_fn=astar_line_change.line_change)

    shortest_path(graph, "Żmudzka", "Kliniki - Politechnika Wrocławska", "16:00:00")
    astar(graph, "Żmudzka", "Kliniki - Politechnika Wrocławska", "16:00:00", heuristic_fn=haversine_distance)
    astar_line(graph, "Żmudzka", "Kliniki - Politechnika Wrocławska", "16:00:00", heuristic_fn=astar_line_change.line_change)

    shortest_path(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00")
    astar(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00", heuristic_fn=haversine_distance)
    astar_line(graph, "GALERIA DOMINIKAŃSKA", "PL. GRUNWALDZKI", "16:27:00", heuristic_fn=astar_line_change.line_change)

    # tabu_search(graph, "Reja", L)
