from cars.autonomous_controlled_car import AutonomousControlledCar
from genetic.chromosome_helper import ChromosomeHelper
from cars.steering_logic.genetic_steering_logic import GeneticSteeringLogic
from genetic.neural_from_internet.autonomous_steering_logic2 import AutonomousSteeringLogic2
import math

class GeneticControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.set_steering_logic(GeneticSteeringLogic())
    self.chromosome_helper = ChromosomeHelper()

  def set_chromosome(self, chromosome):
    AutonomousControlledCar.set_chromosome(self, chromosome)
    weights = self.chromosome_helper.genome_to_decimals(self.chromosome)
    if self.autonomous_steering_logic.number_of_network_weights() != len(weights):
      raise Exception("Invalid number of weights in chromosome")

    self.autonomous_steering_logic.set_neural_weights(weights)
