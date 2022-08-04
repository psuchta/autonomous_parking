import random
from genome_helper import GenomeHelper
import numpy as np

class GeneticHelper:

  def __init__(self):
    self.genome_helper = GenomeHelper()

  def create_generation(self, generation_size, genome_size = GenomeHelper.GENOME_LENGTH):
    return [self.genome_helper.init_randomly(genome_size) for _ in range(generation_size)]

  def crossover(self, parent1, parent2):
    if len(parent1) != len(parent2):
      raise Exception("Lengths of passed arrays are not the same")
    length = len(parent1)
    position = random.randint(2, length-2)
    child1 = parent1[0:position] + parent2[position:length]
    child2 = parent2[0:position] + parent1[position:length]
    return child1, child2

  def tournament_selection(self, population):
    new_population = []
    for j in range(2):
      random.shuffle(population)
      for i in range(0, population_size-1, 2):
        if fitness(graph, population[i]) > fitness(graph, population[i+1]):
          new_population.append(population[i])
        else:
          new_population.append(population[i+1])
    return new_population

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