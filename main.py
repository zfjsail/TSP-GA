from algo.population import init_population, evolve_population
from algo.fitness import cal_dist, get_fittest


init_size = 200
restrict_size = 100
iter_num = 200

tours = init_population(init_size)
print('init distance', cal_dist(get_fittest(tours)))

for i in range(iter_num):
    if i % 10 == 0:
        print(i)
    tours = evolve_population(tours, restrict_size)

best_tour = get_fittest(tours)
print('best', best_tour)
print('final distance', cal_dist(best_tour))
