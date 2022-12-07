from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.neat_controlled_car import NeatControlledCar
from base_program import BaseProgram
from genetic_helper import GeneticHelper
import pygame
import os
import neat

class NeatProgram(BaseProgram):

  def __init__(self):
    BaseProgram.__init__(self)
    self.genetic_helper = GeneticHelper()


  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    for idx in range(30):
      car = NeatControlledCar(700, 430, self.screen, self)
      self.add_car(car)

  def set_genomes(self, genomes, config):
    for idx, genome in enumerate(genomes):
      self.steerable_cars[idx].set_chromosome(genome[1], config)

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def run_generation(self, genomes, config):
    self.set_genomes(genomes, config)
    [car.reset(700, 430) for car in self.steerable_cars]
    time_passed = 0
    start_time = pygame.time.get_ticks()
    while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 15000:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.draw_objects(dt)
      self.draw_generation_num(1)
      # self.genetic_helper.fitness(self.steerable_cars[0], self.parking_slot)
      pygame.display.flip()
      self.clock.tick(self.fps)
      time_passed = pygame.time.get_ticks() - start_time

    self.genetic_helper.calculate_fitness_in_cars(self.steerable_cars, self.parking_slot)

    for car in self.steerable_cars:
      car.chromosome.fitness = car.fitness

  def run_neat(self, config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    winner = p.run(self.run_generation, 10)

  def run(self):
    local_dir = os.path.dirname(__file__)
    print(local_dir)
    config_path = os.path.join(local_dir, 'settings.txt')
    self.run_neat(config_path)

