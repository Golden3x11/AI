import time
from functools import wraps

import matplotlib.pyplot as plt


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


def print_moves_graph(title, moves_list):
    values = moves_list[1:]
    moves = [i + 1 for i in range(len(values))]
    plt.plot(moves, values)
    plt.title(title)
    plt.xlabel('Move number')
    plt.ylabel('Number of nodes visited')
    plt.show()
