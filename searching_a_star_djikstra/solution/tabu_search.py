import math
import random

import util

def get_distances(graph, stops):
    distances = {}
    total = 0
    for start in stops:
        distances[start] = {}
        for end in stops:
            dist = util.haversine_distance(graph[start]["start_pos"], graph[end]["start_pos"])
            distances[start][end] = dist
            total += dist

    return distances, total


def tabu_search(graph, start, stops: list):
    stops.append(start)
    n_stops = len(stops)
    distances, total = get_distances(graph, stops)
    stops.remove(start)

    max_iterations = math.ceil(1.1 * (n_stops ** 2))
    turns_improved = 0
    improve_thresh = 2 * math.floor(math.sqrt(max_iterations))
    tabu_list = []
    tabu_tenure = n_stops
    aspiration_criteria = (total / (n_stops ** 2)) * 2.2

    current_solution = stops
    random.shuffle(current_solution)
    current_solution.insert(0, start)

    best_solution = current_solution[:]
    best_solution_cost = sum([distances[current_solution[i]][current_solution[(i+1)%n_stops]] for i in range(n_stops)])

    for iteration in range(max_iterations):
        if turns_improved > improve_thresh:
            break
        best_neighbor = None
        best_neighbor_cost = float('inf')
        tabu_candidate = (None, None)

        for i in range(n_stops):
            for j in range(i+1, n_stops):
                neighbor = current_solution[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbor_cost = sum([distances[neighbor[i]][neighbor[(i+1)%n_stops]] for i in range(n_stops)])
                if (i, j) not in tabu_list or neighbor_cost < aspiration_criteria:
                    if neighbor_cost < best_neighbor_cost:
                        best_neighbor = neighbor[:]
                        best_neighbor_cost = neighbor_cost
                        tabu_candidate = (i, j)

        if best_neighbor is not None:
            current_solution = best_neighbor[:]
            tabu_list.append(tabu_candidate)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            if best_neighbor_cost < best_solution_cost:
                best_solution = best_neighbor[:]
                best_solution_cost = best_neighbor_cost
                turns_improved = 0
            else:
                turns_improved += 1

        print("Iteration {}: Best solution cost = {}".format(iteration, best_solution_cost))

    print("Best solution: {}".format(best_solution))
    print("Best solution cost: {}".format(best_solution_cost))



