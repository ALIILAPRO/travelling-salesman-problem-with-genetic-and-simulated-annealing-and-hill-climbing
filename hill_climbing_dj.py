import random
import copy

import numpy as np
from numpy.linalg import norm


class State:
    def __init__(self, route: [], distance: int = 0):
        self.route = route
        self.distance = distance

    def __eq__(self, other):
        for i in range(len(self.route)):
            if self.route[i] != other.route[i]:
                return False
        return True

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        return "({0},{1})\n".format(self.route, self.distance)

    def copy(self):
        return State(self.route, self.distance)

    def deepcopy(self):
        return State(copy.deepcopy(self.route), copy.deepcopy(self.distance))

    def update_distance(self, matrix, home):
        self.distance = 0
        from_index = home
        for i in range(len(self.route)):
            self.distance += matrix[from_index][self.route[i]]
            from_index = self.route[i]
        self.distance += matrix[from_index][home]


class City:
    def __init__(self, index: int, distance: int):
        self.index = index
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance

def get_random_solution(matrix:[], home:int, city_indexes:[], size:int):
    cities = city_indexes.copy()
    cities.pop(home)
    population = []
    for i in range(size):
        random.shuffle(cities)
        state = State(cities[:])
        state.update_distance(matrix, home)
        population.append(state)
    population.sort()
    return population[0]

def mutate(matrix: [], home: int, state: State, mutation_rate: float = 0.01):
    mutated_state = state.deepcopy()
    for i in range(len(mutated_state.route)):
        if random.random() < mutation_rate:
            j = int(random.random() * len(state.route))
            city_1 = mutated_state.route[i]
            city_2 = mutated_state.route[j]
            mutated_state.route[i] = city_2
            mutated_state.route[j] = city_1
    mutated_state.update_distance(matrix, home)
    return mutated_state


def hill_climbing(
    matrix: [],
    home: int,
    initial_state: State,
    max_iterations: int,
    mutation_rate: float = 0.01,
):
    best_state = initial_state
    iterator = 0
    while True:
        neighbor = mutate(matrix, home, best_state, mutation_rate)
        if neighbor.distance >= best_state.distance:
            iterator += 1
            if iterator > max_iterations:
                break
        if neighbor.distance < best_state.distance:
            best_state = neighbor
    return best_state


def get_euclidean_distance(p, q):
    return round(norm(np.array(p) - np.array(q)))


def main():

    cities_coordinates = {
        1: (11003.611100, 42102.500000),
2: (11108.611100, 42373.888900), 
3: (11133.333300, 42885.833300), 
4: (11155.833300, 42712.500000), 
5: (11183.333300, 42933.333300), 
6: (11297.500000, 42853.333300), 
7: (11310.277800, 42929.444400), 
8: (11416.666700, 42983.333300), 
9: (11423.888900, 43000.277800), 
10: (11438.333300, 42057.222200),
11: (11461.111100, 43252.777800),
12: (11485.555600, 43187.222200),
13: (11503.055600, 42855.277800),
14: (11511.388900, 42106.388900),
15: (11522.222200, 42841.944400),
16: (11569.444400, 43136.666700),
17: (11583.333300, 43150.000000),
18: (11595.000000, 43148.055600),
19: (11600.000000, 43150.000000),
20: (11690.555600, 42686.666700),
21: (11715.833300, 41836.111100),
22: (11751.111100, 42814.444400),
23: (11770.277800, 42651.944400),
24: (11785.277800, 42884.444400),
25: (11822.777800, 42673.611100),
26: (11846.944400, 42660.555600),
27: (11963.055600, 43290.555600),
28: (11973.055600, 43026.111100),
29: (12058.333300, 42195.555600),
30: (12149.444400, 42477.500000),
31: (12286.944400, 43355.555600),
32: (12300.000000, 42433.333300),
33: (12355.833300, 43156.388900),
34: (12363.333300, 43189.166700),
35: (12372.777800, 42711.388900),
36: (12386.666700, 43334.722200),
37: (12421.666700, 42895.555600),
38: (12645.000000, 42973.333300),
    }

    D = []
    for _, target_coordinates in cities_coordinates.items():
        distances = []
        for _, coordinates in cities_coordinates.copy().items():
            distances.append(get_euclidean_distance(target_coordinates, coordinates))
        D.append(distances)

    home = 0
    max_iterations = 100000
    cities = list(cities_coordinates.keys())
    city_indexes = [index - 1 for index in cities]

    state = get_random_solution(D, home, city_indexes, 100)
    print("Travelling Salesman Problem: Djibouti Edition\n")
    print("-- Initial state solution --")
    print(cities[home], end="")
    for i in range(0, len(state.route)):
        print(" -> " + str(cities[state.route[i]]), end="")
    print(" -> " + str(cities[home]), end="")
    print("\n\nTotal distance: {0} miles".format(state.distance))
    print()

    state = hill_climbing(D, home, state, max_iterations, 0.1)
    print("-- Hill climbing solution --")
    print(cities[home], end="")
    for i in range(0, len(state.route)):
        print(" -> " + str(cities[state.route[i]]), end="")
    print(" -> " + str(cities[home]), end="")
    print("\n\nTotal distance: {0} miles".format(state.distance))
    print()


if __name__ == "__main__":
    main()