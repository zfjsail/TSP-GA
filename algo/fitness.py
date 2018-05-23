import math
from utils.data_utils import city_dict, city_num


def cal_dist(tour):
    total_dist = 0
    for i, city in enumerate(tour):
        cur_loc = city_dict[city]
        if i+1 < city_num:
            next_loc = city_dict[tour[i+1]]
        else:
            next_loc = city_dict[tour[0]]
        delta_x = next_loc['x'] - cur_loc['x']
        delta_y = next_loc['y'] - cur_loc['y']
        cur_dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
        total_dist += cur_dist
    return total_dist


def get_fitness(tour):
    total_dist = cal_dist(tour)
    return 1 / total_dist


def get_fittest(tours):
    fittest_tour = tours[0]
    fittest_score = get_fitness(tours[0])
    for i in range(1, len(tours)):
        cur_fitness = get_fitness(tours[i])
        if cur_fitness > fittest_score:
            fittest_tour = tours[i]
            fittest_score = cur_fitness
    return fittest_tour
