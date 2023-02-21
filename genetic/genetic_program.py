from base_program import BaseProgram
from genetic.genetic_helper import GeneticHelper
from genetic.chromosome_helper import ChromosomeHelper
from cars.genetic_controlled_car import GeneticControlledCar
import numpy as np
import pygame
import random
from genetic.settings import settings

class GeneticProgram(BaseProgram):
  def __init__(self):
    self.settings = settings
    self.genetic_helper = GeneticHelper()
    self.chromosome_helper = ChromosomeHelper()
    BaseProgram.__init__(self)

  def set_cars_chromosomes(self, chromosome_array):
    if len(self.steerable_cars) != len(chromosome_array):
      raise Exception("Lengths of passed arrays are not the same")

    for idx, chromosome in enumerate(chromosome_array):
      self.steerable_cars[idx].set_chromosome(chromosome)

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    for idx in range(self.settings['population_size']):
      car = GeneticControlledCar(700, 430, self.screen, self)
      self.add_car(car)

    numbers_per_chromosome = car.autonomous_steering_logic.number_of_network_weights()
    chromosome_array = self.genetic_helper.create_random_generation(self.settings['population_size'], numbers_per_chromosome=numbers_per_chromosome)
    self.set_cars_chromosomes(chromosome_array)

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
    selected_population = None
    if self.settings['selection_method'] == 'tournament':
      # tournament_size = self.genetic_helper.population_procentage(population, self.settings['tournament_procentage'])
      tournament_size = self.settings['tournament_size']
      selected_population = self.genetic_helper.tournament_selection(population, tournament_size)
    elif self.settings['selection_method'] == 'roulette':
      selected_population = self.genetic_helper.roulette_wheel_selection(population)
    new_population = []
    random.shuffle(selected_population)
    for i in range(0, len(selected_population)-1, 2):
      if random.uniform(0, 1) <= self.settings['crossover_probability']:
        child1, child2 = self.genetic_helper.crossover(selected_population[i].chromosome, selected_population[i+1].chromosome)
      else:
        child1, child2 = selected_population[i].chromosome.copy(), selected_population[i+1].chromosome.copy()
      self.genetic_helper.mutate_chromosome(child1, self.settings['mutation_probability'])
      self.genetic_helper.mutate_chromosome(child2, self.settings['mutation_probability'])

      new_population.append(child1)
      new_population.append(child2)

    return new_population

  # Population is divided into specified number of segments. Breeding sequence is executed on each segment separately.
  def breed_with_segments(self, population):
    population.sort(key=lambda x: x.fitness, reverse=True)
    divided_population = np.array_split(population, 2)
    new_population = []
    for local_population in divided_population:
      new_population.extend(self.breed(local_population.tolist()))
    return new_population

  def save_population_to_file(self, population, file_name="last_population"):
    chromosomes = [car.chromosome for car in population]
    data = np.asarray(chromosomes)
    np.savetxt(f'genetic/{file_name}.csv', data, fmt='%i', delimiter=',')

  def laod_population_from_file(self, file_name="last_population"):
    data = np.loadtxt(f'genetic/{file_name}.csv', dtype='int', delimiter=',')
    self.set_cars_chromosomes(data.tolist())

  def run(self):
    # best_fitness_car[0] - fitness_score
    # best_fitness_car[1] - chromosome of the best car
    best_fitness_car = (None, None)
    generation_size = 2000
    # self.laod_population_from_file()
    for g in range(generation_size):
      if self.exit: break
      self.run_generation(g)
      self.genetic_helper.calculate_fitness_in_cars(self.steerable_cars, self.parking_slot)

      best_fitness_car = self.genetic_helper.set_best_individual(self.steerable_cars, best_fitness_car)
      if self.settings['breeding_method'] == 'default':
        new_population = self.breed(self.steerable_cars)
      elif self.settings['breeding_method'] == 'segments':
        new_population = self.breed_with_segments(self.steerable_cars)

      if self.settings['add_previous_best'] == True:
        self.genetic_helper.copy_best_to_population(new_population, best_fitness_car[1])
      self.set_cars_chromosomes(new_population)
      [car.reset(700, 430) for car in self.steerable_cars]
    print("Best car in simulation")
    print(best_fitness_car[0])
    print(best_fitness_car[1])
    print(self.chromosome_helper.genome_to_decimals(best_fitness_car[1]))
    # self.save_population_to_file(self.steerable_cars)
    pygame.quit()
