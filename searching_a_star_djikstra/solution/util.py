import statistics
from collections import namedtuple
from functools import wraps
import time


Cords = namedtuple("Cords", ["X", "Y"])
NextStop = namedtuple("NextStop", ["name", "cords", "line", "departure", "arrival"])


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

def update_start_pos(graph):
    for start, data in graph.items():
        start_pos_list = list(data["start_pos"])
        if len(start_pos_list) > 0:
            avg_pos = Cords(statistics.mean(pos.X for pos in start_pos_list),
                               statistics.mean(pos.Y for pos in start_pos_list))
            data["start_pos"] = avg_pos