import random
import numpy as np
from copy import deepcopy
from algo.fitness import get_fitness
from utils.data_utils import city_list, city_num
from utils.sample import alias_setup, alias_draw


def init_population(init_sz):
    tours = []
    for i in range(init_sz):
        cur_tour = deepcopy(city_list)
        random.shuffle(cur_tour)
        tours.append(cur_tour)
    return tours


def select(tours, restrict_size, elitism=True):
    unnorm_fitnesses = [get_fitness(tour) for tour in tours]
    sum_fitness = sum(unnorm_fitnesses)
    norm_probs = [fitness/sum_fitness for fitness in unnorm_fitnesses]
    J, q = alias_setup(norm_probs)

    new_tours = []
    start_idx = 0
    if elitism:
        fittest_idx = np.argmax(unnorm_fitnesses)
        new_tours.append(tours[fittest_idx])
        start_idx += 1

    for i in range(start_idx, restrict_size):
        sampled_idx = alias_draw(J, q)
        new_tours.append(tours[sampled_idx])
    return new_tours


def tournament_selection(tours, fitness_scores, tournament_size):
    sampled_indices = np.random.choice(len(tours), tournament_size)
    fitness_scores = np.array(fitness_scores)
    sampled_fitness_scores = fitness_scores[sampled_indices]
    max_idx_in_sampled = np.argmax(sampled_fitness_scores)
    max_idx_orig = sampled_indices[max_idx_in_sampled]
    assert fitness_scores[max_idx_orig] == sampled_fitness_scores[max_idx_in_sampled]
    return max_idx_orig


def find_next_available_idx(tour, start=0):
    while tour[start] is not None:
        start += 1
    assert start < city_num
    return start


def crossover(tour1, tour2):
    new_tour = [None] * city_num

    start_pos = int(np.floor(np.random.rand()*city_num))
    end_pos = int(np.floor(np.random.rand()*city_num))

    for i in range(city_num):
        if start_pos < end_pos and start_pos < i < end_pos:
            new_tour[i] = tour1[i]
        elif start_pos > end_pos:
            if i >= start_pos or i <= end_pos:
                new_tour[i] = tour1[i]

    next_available_idx = 0
    for i in range(city_num):
        child_have_now = set(new_tour)
        if tour2[i] not in child_have_now:
            next_available_idx = find_next_available_idx(new_tour, next_available_idx)
            new_tour[next_available_idx] = tour2[i]
    return new_tour


def mutate(tour, mutatation_rate):
    for pos1 in range(city_num):
        if np.random.rand() < mutatation_rate:
            pos2 = int(np.floor(np.random.rand()*city_num))
            tmp = tour[pos1]
            tour[pos1] = tour[pos2]
            tour[pos2] = tmp
    return tour


def evolve_population(tours, restrict_size, elitism=True, tournament_size=5, mutatation_rate=0.015):
    init_size = len(tours)
    new_tours1 = select(tours, restrict_size, elitism)

    new_tours2 = deepcopy(new_tours1)
    fitness_scores_newtour1 = [get_fitness(tour) for tour in new_tours1]
    for i in range(restrict_size, init_size):
        idx1 = tournament_selection(new_tours1, fitness_scores_newtour1, tournament_size)
        idx2 = tournament_selection(new_tours1, fitness_scores_newtour1, tournament_size)
        tour1, tour2 = new_tours1[idx1], new_tours1[idx2]
        child = crossover(tour1, tour2)
        new_tours2.append(child)
    assert len(new_tours2) == init_size

    start_idx = 0
    if elitism:
        start_idx = 1
    new_tours3 = deepcopy(new_tours2)
    for i in range(start_idx, init_size):
        new_tours3[i] = mutate(new_tours2[i], mutatation_rate)
    return new_tours3


if __name__ == '__main__':
    tours = init_population(5)
    for tour in tours:
        print(tour)
