from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.neat_controlled_car import NeatControlledCar
from base_program import BaseProgram
from genetic.genetic_helper import GeneticHelper
from genetic.genetic_program import GeneticProgram
import pygame
import os
import neat

class NeatProgram(GeneticProgram):

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

  def run_generation(self, genomes, config):
    self.set_genomes(genomes, config)
    [car.reset(700, 430) for car in self.steerable_cars]
    # Call parent's class function
    GeneticProgram.run_generation(self, 1)

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

    winner = p.run(self.run_generation, 100)

  def run(self):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'settings.txt')
    self.run_neat(config_path)

