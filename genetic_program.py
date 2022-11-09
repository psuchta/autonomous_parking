from base_program import BaseProgram
from genetic_helper import GeneticHelper
from genome_helper import GenomeHelper
from cars.autonomous_controlled_car import AutonomousControlledCar
import numpy as np
import pygame
import random

GENERATION_SIZE = 80
MUTATION_PROBABILITY = 0.01

class GeneticProgram(BaseProgram):
  def __init__(self):
    self.genetic_helper = GeneticHelper()
    self.genome_helper = GenomeHelper()
    BaseProgram.__init__(self)

  def set_cars_genomes(self, genome_array):
    print('print genome')
    print(len(genome_array))
    if len(self.steerable_cars) != len(genome_array):
      raise Exception("Lengths of passed arrays are not the same")

    idx = 0
    for genome in genome_array:
      self.steerable_cars[idx].set_genome(genome)
      idx += 1

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    for idx in range(GENERATION_SIZE):
      car = AutonomousControlledCar(700, 430, self.screen, self)
      self.add_car(car)

    numbers_per_genome = car.autonomous_steering_logic.number_of_network_weights()
    genome_array = self.genetic_helper.create_random_generation(GENERATION_SIZE, numbers_per_genome=numbers_per_genome)
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

  def breed(self, best_fitness_car):
    local_best_car = self.genetic_helper.best_fitness_car(self.steerable_cars)
    if best_fitness_car[0] == None or (best_fitness_car[0] < local_best_car.fitness):
      best_fitness_car = (local_best_car.fitness, local_best_car.genome)

    selected_population = self.genetic_helper.tournament_selection(self.steerable_cars, 30)
    # selected_population = self.genetic_helper.roulette_wheel_selection(fitness_results, self.steerable_cars)
    new_population = []
    for i in range(0, len(selected_population)-1, 2):
      child1, child2 = self.genetic_helper.crossover_ieee_754(selected_population[i].genome, selected_population[i+1].genome)
      self.genetic_helper.mutate_ieee_754_genome(child1, MUTATION_PROBABILITY)
      self.genetic_helper.mutate_ieee_754_genome(child2, MUTATION_PROBABILITY)

      new_population.append(child1)
      new_population.append(child2)

    if not any(genome == best_fitness_car[1] for genome in new_population):
      print('copy best')
      new_population[random.randrange(len(new_population))] = best_fitness_car[1]

    return new_population

  def breed_pop(self, population, tournament_procentage = 0.3):
    selected_population = self.genetic_helper.tournament_selection(population, int(len(population) * tournament_procentage))
    # selected_population = self.genetic_helper.roulette_wheel_selection(fitness_results, self.steerable_cars)
    new_population = []
    for i in range(0, len(selected_population)-1, 2):
      child1, child2 = self.genetic_helper.crossover_ieee_754(selected_population[i].genome, selected_population[i+1].genome)
      self.genetic_helper.mutate_ieee_754_genome(child1, MUTATION_PROBABILITY)
      self.genetic_helper.mutate_ieee_754_genome(child2, MUTATION_PROBABILITY)

      new_population.append(child1)
      new_population.append(child2)

    return new_population

  def run(self):
    # best_fitness_car[0] - fitness_score
    # best_fitness_car[1] - genome of the best car
    best_fitness_car = (None, None)
    generation_size = 500
    for g in range(generation_size):
      if self.exit: break
      self.run_generation(g)
      self.genetic_helper.calculate_fitness_in_cars(self.steerable_cars, self.parking_slot)
      self.steerable_cars.sort(key=lambda x: x.fitness, reverse=True)
      local_best_car = self.genetic_helper.best_fitness_car(self.steerable_cars)
      if best_fitness_car[0] == None or (best_fitness_car[0] < local_best_car.fitness):
        best_fitness_car = (local_best_car.fitness, local_best_car.genome)

      divided_population = np.array_split(self.steerable_cars, 4)
      new_population = []
      for population in divided_population:
        new_population.extend(self.breed_pop(population.tolist()))

      # if not any(genome == best_fitness_car[1] for genome in new_population):
      #   print('copy best')
      #   new_population[random.randrange(len(new_population))] = best_fitness_car[1]

      self.set_cars_genomes(new_population)
      [car.reset(700, 430) for car in self.steerable_cars]
    print(best_fitness_car[0])
    print(best_fitness_car[1])
    print(self.genome_helper.genome_to_decimals(best_fitness_car[1]))
    pygame.quit()
