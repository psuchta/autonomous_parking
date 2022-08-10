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

  def create_random_generation(self, generation_size, genome_size = GenomeHelper.GENOME_LENGTH):
    return [self.genome_helper.init_randomly(genome_size) for _ in range(generation_size)]

  def crossover(self, parent1, parent2):
    if len(parent1) != len(parent2):
      raise Exception("Lengths of passed arrays are not the same - Crossover")
    length = len(parent1)
    position = random.randint(2, length-2)
    child1 = parent1[0:position] + parent2[position:length]
    child2 = parent2[0:position] + parent1[position:length]
    return child1, child2

  def tournament_selection(self, fitness_results, car_population, parking_spot, tournament_size):
    if tournament_size > len(car_population):
      raise Exception("Tournament size is greater than car population")

    selected = []
    population_size = len(car_population)
    
    for idx in range(population_size):
      tournament_population_idx = random.sample(list(range(population_size)), tournament_size)
      max_fit_index = max(tournament_population_idx, key=lambda idx: fitness_results[idx])
      selected.append(car_population[max_fit_index])

    return selected

  def roulette_wheel_selection(self, graph, population):
      new_population = []

      fitness_array = [fitness(graph, c) for c in population]
      min_in_fitness = min(fitness_array)
      fitness_array = [f - min_in_fitness for f in fitness_array]
      max_fitness = sum(fitness_array)

      selection_probs = [f/max_fitness for f in fitness_array]
      for i in range(len(population)):
        new_population.append(population[np.random.choice(len(population), p=selection_probs)])

      return new_population

  def mutate_genome(self, binary_genome, probability=0.1):
    for idx, val in enumerate(binary_genome):
      if random.uniform(0, 1) <= probability:
        # change to opposite binary val
        binary_genome[idx] = 1 - val

  def fitness(self, car, parking_spot):
    distance_loss = car.distance_to_point(parking_spot.rect.center)
    distance_fitness = 1 - (distance_loss/6.5)
    intersection_fintness = parking_spot.car_intersection_ratio(car.rect)
    return (distance_fitness + intersection_fintness)/2
