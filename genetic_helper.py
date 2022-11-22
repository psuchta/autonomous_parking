import random
from genome_helper import GenomeHelper
import pygame
import numpy as np

class GeneticHelper:

  def __init__(self):
    self.genome_helper = GenomeHelper()

  def population_procentage(self, population, procentage):
    return int(len(population) * procentage)

  def set_best_individual(self, population, global_best):
    local_best_car = self.best_fitness_car(population)
    print(f'{global_best[0]} {local_best_car.fitness}')
    if global_best[0] == None or (global_best[0] < local_best_car.fitness):
      return (local_best_car.fitness, local_best_car.genome.copy())

    return global_best

  def copy_best_to_population(self, population, best_genome):
    if not any(genome == best_genome for genome in population):
      print('Copy best to the next generation')
      population[random.randrange(len(population))] = best_genome.copy()

  def calculate_fitness_in_cars(self, car_population, parking_spot):
    for car in car_population: self.fitness(car, parking_spot)

  def best_fitness_car(self, car_population):
    car = max(car_population, key=lambda car: car.fitness)
    return  car

  def create_random_generation(self, population_size, numbers_per_genome):
    return [self.genome_helper.init_randomly(numbers_per_genome) for _ in range(population_size)]

  def crossover_ieee_754(self, parent1, parent2):
    child1, child2 = self.crossover(parent1, parent2)
    # Check if children dont't contain any Nan or Infinity
    while self.genome_helper.check_if_any_number_forbidden(child1) or self.genome_helper.check_if_any_number_forbidden(child2) :
      child1, child2 = self.crossover(parent1, parent2)
    return child1, child2

  def crossover(self, parent1, parent2):
    if len(parent1) != len(parent2):
      raise Exception("Lengths of passed arrays are not the same - Crossover")
    length = len(parent1)
    position = random.randint(2, length-2)
    child1 = parent1[0:position] + parent2[position:length]
    child2 = parent2[0:position] + parent1[position:length]
    return child1, child2

  def tournament_selection(self, car_population, tournament_size):
    if tournament_size > len(car_population):
      raise Exception("Tournament size is greater than car population")

    selected = []
    population_size = len(car_population)
    
    for idx in range(population_size):
      tournament_population = random.sample(car_population, tournament_size)
      max_car = max(tournament_population, key=lambda car: car.fitness)
      selected.append(max_car)

    return selected

  def roulette_wheel_selection(self, car_population):
      new_population = []
      car_population.sort(key=lambda x: x.fitness, reverse=True)
      # Descending order
      fitness_results = [car.fitness for car in car_population]
      # Get rid off negative fitnesses
      min_in_fitness = fitness_results[-1]
      fitness_results = [fitness - min_in_fitness for fitness in fitness_results]

      max_fitness = sum(fitness_results)

      selection_probs = [fitness/max_fitness for fitness in fitness_results]
      for i in range(len(car_population)):
        new_population.append(car_population[np.random.choice(len(car_population), p=selection_probs)])

      return new_population

  def mutate_ieee_754_genome(self, binary_genome, probability):
    new_genome = []
    # Iterate over all numbers in the genome
    # in the genome each number has length of 16 bits
    for idx in range(0, len(binary_genome), GenomeHelper.GENES_PER_NUMBER):
      binary_number = binary_genome[idx:idx+GenomeHelper.GENES_PER_NUMBER]

      self.mutate_genome(binary_number, probability)
      # Repeat mutation process on original number until binary isn't Nan or Inifinity
      while self.genome_helper.check_if_number_forbidden(binary_number):
        binary_number = binary_genome[idx:idx+GenomeHelper.GENES_PER_NUMBER]
        self.mutate_genome(binary_number, probability)
      new_genome.extend(binary_number)
    binary_genome[:] = new_genome

  def mutate_genome(self, binary_genome, probability):
    for idx, val in enumerate(binary_genome):
      if random.uniform(0, 1) <= probability:
        # change to opposite binary val
        binary_genome[idx] = 1 - val

  def fitness(self, car, parking_spot):
    distance_loss = car.distance_to_point(parking_spot.rect.center)
    distance_loss = car.distance_to_parking(parking_spot)
    fitness = 1/(distance_loss+1)
    if not car.alive:
      fitness -= 0.1

    car.fitness = fitness
    return fitness
