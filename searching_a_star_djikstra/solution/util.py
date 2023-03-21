import statistics
import time
from collections import namedtuple
from functools import wraps
from itertools import groupby

from haversine import haversine

Cords = namedtuple("Cords", ["X", "Y"])
NextStop = namedtuple("NextStop", ["idx", "name", "cords", "line", "departure", "arrival"])


def convert_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def convert_to_time_string(total_seconds):
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def print_stops(path):
    groups = groupby(path, key=lambda stop: stop[1])
    print('-' * 106)
    print(f"{'Line':<5}{'Start':<40}{'End':<40}{'Arrival':<10}{'Departure':<10}|")
    print('-' * 106)

    for line, group in groups:
        group_list = list(group)
        start = group_list[0]
        end = group_list[-1]
        print(f"{line:<5}{start[0]:<40}{end[4]:<40}{start[2]:<10}{end[3]:<10}|")

    print('-' * 106)


def print_results_astar(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        heuristic_fn = kwargs.get('heuristic_fn')
        cost, path = func(*args, **kwargs)
        print(f"Cost using {heuristic_fn.__name__} heuristic: {convert_to_time_string(cost)}")
        print(f"Path using {heuristic_fn.__name__} heuristic:")
        print_stops(path)
        print()
        return cost, path

    return wrapper


def print_results_djikstra(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cost, path = func(*args, **kwargs)
        print("Shortest cost:", convert_to_time_string(cost))
        print("Shortest path:")
        print_stops(path)
        print()
        return cost, path

    return wrapper


def update_start_pos(graph):
    for start, data in graph.items():
        start_pos_list = list(data["start_pos"])
        if len(start_pos_list) > 0:
            avg_pos = Cords(statistics.mean(pos.X for pos in start_pos_list),
                            statistics.mean(pos.Y for pos in start_pos_list))
            data["start_pos"] = avg_pos


def haversine_distance(cords1, cords2):
    return haversine(cords1, cords2)
