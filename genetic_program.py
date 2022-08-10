from base_program import BaseProgram
from genetic_helper import GeneticHelper
from cars.autonomous_controlled_car import AutonomousControlledCar
import pygame

GENERATION_SIZE = 10
MUTATION_PROBABILITY = 0.04

class GeneticProgram(BaseProgram):
  def __init__(self):
    self.genetic_helper = GeneticHelper()
    BaseProgram.__init__(self)

  def set_cars_genomes(self, genome_array):
    if len(self.steerable_cars) != len(genome_array):
      raise Exception("Lengths of passed arrays are not the same")

    idx = 0
    for genome in genome_array:
      self.steerable_cars[idx].set_genome(genome)
      idx += 1

  def add_game_objects(self):
    BaseProgram.add_game_objects(self)
    genome_array = self.genetic_helper.create_random_generation(GENERATION_SIZE)

    for idx in range(GENERATION_SIZE):
      self.add_car(AutonomousControlledCar(700, 430, self.screen, self))
    self.set_cars_genomes(genome_array)

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def run_generation(self, gen_num):
    time_passed = 0
    start_time = pygame.time.get_ticks()
    while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <=10000:
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


  def run(self):
    # best_fitness_car[0] - fitness_score
    # best_fitness_car[1] - genome of the best car
    best_fitness_car = (None, None)
    generation_size = 50
    for g in range(generation_size):
      if self.exit: break
      self.run_generation(g)
      fitness_results = self.genetic_helper.extract_fitness_from_cars(self.steerable_cars, self.parking_slot)
      local_best_fitness = self.genetic_helper.best_fitness_index(fitness_results, self.steerable_cars)
      if best_fitness_car[0] == None or (best_fitness_car[0] < local_best_fitness[0]):
        best_fitness_car = local_best_fitness

      selected_population = self.genetic_helper.tournament_selection(fitness_results, self.steerable_cars, self.parking_slot, 3)
      new_population = []
      for i in range(0, len(selected_population)-1, 2):
        child1, child2 = self.genetic_helper.crossover(selected_population[i].genome, selected_population[i+1].genome)
        self.genetic_helper.mutate_genome(child1, MUTATION_PROBABILITY)
        self.genetic_helper.mutate_genome(child2, MUTATION_PROBABILITY)
        new_population.append(child1)
        new_population.append(child2)
        # if len(new_population) < GENERATION_SIZE:
          # new_population.append(child2)
      self.set_cars_genomes(new_population)
      [car.reset(700, 430) for car in self.steerable_cars]
    pygame.quit()
