from base_program import BaseProgram
from genetic_helper import GeneticHelper
from genome_helper import GenomeHelper
from cars.autonomous_controlled_car import AutonomousControlledCar
import numpy as np
import pygame
import random

POPULATION_SIZE = 50
MUTATION_PROBABILITY = 0.01
CROSSOVER_PROBABILITY = 0.3
TOURNAMENT_PROCENTAGE = 0.4

class GeneticProgram(BaseProgram):
  def __init__(self):
    self.genetic_helper = GeneticHelper()
    self.genome_helper = GenomeHelper()
    BaseProgram.__init__(self)

  def set_cars_genomes(self, genome_array):
    if len(self.steerable_cars) != len(genome_array):
      raise Exception("Lengths of passed arrays are not the same")

    idx = 0
    for genome in genome_array:
      self.steerable_cars[idx].set_genome(genome)
      idx += 1

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    for idx in range(POPULATION_SIZE):
      car = AutonomousControlledCar(700, 430, self.screen, self)
      self.add_car(car)

    numbers_per_genome = car.autonomous_steering_logic.number_of_network_weights()
    genome_array = self.genetic_helper.create_random_generation(POPULATION_SIZE, numbers_per_genome=numbers_per_genome)
    self.set_cars_genomes(genome_array)

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def run_generation(self, gen_num):
    time_passed = 0
    start_time = pygame.time.get_ticks()
    while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 15000:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.draw_objects(dt)
      self.draw_generation_num(gen_num)
      # self.genetic_helper.fitness(self.steerable_cars[0], self.parking_slot)
      pygame.display.flip()
      self.clock.tick(self.fps)
      time_passed = pygame.time.get_ticks() - start_time

  def breed(self, population):
    tournament_size = self.genetic_helper.population_procentage(population, TOURNAMENT_PROCENTAGE)
    selected_population = self.genetic_helper.tournament_selection(population, tournament_size)
    # selected_population = self.genetic_helper.roulette_wheel_selection(population)
    new_population = []
    for i in range(0, len(selected_population)-1, 2):
      if random.uniform(0, 1) <= CROSSOVER_PROBABILITY:
        child1, child2 = self.genetic_helper.crossover_ieee_754(selected_population[i].genome, selected_population[i+1].genome)
      else:
        child1, child2 = selected_population[i].genome.copy(), selected_population[i+1].genome.copy()
      self.genetic_helper.mutate_ieee_754_genome(child1, MUTATION_PROBABILITY)
      self.genetic_helper.mutate_ieee_754_genome(child2, MUTATION_PROBABILITY)

      new_population.append(child1)
      new_population.append(child2)

    return new_population

  # Population is divided into specified number of segments. Breeding sequence is executed on each segment separately.
  def breed_with_segments(self, population):
    divided_population = np.array_split(population, 4)
    new_population = []
    for local_population in divided_population:
      new_population.extend(self.breed(local_population.tolist()))
    return new_population

  def save_population_to_file(self, population, file_name="last_population"):
    genomes = [car.genome for car in population]
    data = np.asarray(genomes)
    np.savetxt(f'genetic/{file_name}.csv', data, fmt='%i', delimiter=',')

  def laod_population_from_file(self, file_name="last_population"):
    data = np.loadtxt(f'genetic/{file_name}.csv', dtype='int', delimiter=',')
    self.set_cars_genomes(data.tolist())

  def run(self):
    # best_fitness_car[0] - fitness_score
    # best_fitness_car[1] - genome of the best car
    best_fitness_car = (None, None)
    generation_size = 2000
    self.laod_population_from_file()
    for g in range(generation_size):
      if self.exit: break
      self.run_generation(g)
      self.genetic_helper.calculate_fitness_in_cars(self.steerable_cars, self.parking_slot)
      self.steerable_cars.sort(key=lambda x: x.fitness, reverse=True)

      best_fitness_car = self.genetic_helper.set_best_individual(self.steerable_cars, best_fitness_car)
      new_population = self.breed(self.steerable_cars)
      # new_population = self.breed_with_segments(self.steerable_cars)
      self.genetic_helper.copy_best_to_population(new_population, best_fitness_car[1])
      self.set_cars_genomes(new_population)
      [car.reset(700, 430) for car in self.steerable_cars]
    print("Best car in simulation")
    print(best_fitness_car[0])
    print(best_fitness_car[1])
    print(self.genome_helper.genome_to_decimals(best_fitness_car[1]))
    self.save_population_to_file(self.steerable_cars)
    pygame.quit()
