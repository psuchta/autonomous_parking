import random
from genome_helper import GenomeHelper
import pygame
import numpy as np

class GeneticHelper:

  def __init__(self):
    self.genome_helper = GenomeHelper()

  def extract_fitness_from_cars(self, car_population, parking_spot):
    return [self.fitness(car, parking_spot) for car in car_population]

  def best_fitness_index(self, fitness_results, car_population):
    max_fitness_index = max(range(len(car_population)), key=lambda idx: fitness_results[idx])
    return  fitness_results[max_fitness_index], car_population[max_fitness_index].genome

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

  def tournament_selection(self, fitness_results, car_population, tournament_size):
    if tournament_size > len(car_population):
      raise Exception("Tournament size is greater than car population")

    selected = []
    population_size = len(car_population)
    
    for idx in range(population_size):
      tournament_population_idx = random.sample(list(range(population_size)), tournament_size)
      max_fit_index = max(tournament_population_idx, key=lambda idx: fitness_results[idx])
      selected.append(car_population[max_fit_index])

    return selected

  def roulette_wheel_selection(self, fitness_results, population):
      new_population = []

      min_in_fitness = min(fitness_results)
      fitness_results = [f - min_in_fitness for f in fitness_results]
      max_fitness = sum(fitness_results)

      selection_probs = [f/max_fitness for f in fitness_results]
      for i in range(len(population)):
        new_population.append(population[np.random.choice(len(population), p=selection_probs)])

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
    print(fitness)
    return fitness
