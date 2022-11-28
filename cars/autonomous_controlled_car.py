from cars.controlled_car import ControlledCar
from chromosome_helper import ChromosomeHelper
from autonomous_steering_logic import AutonomousSteeringLogic
from neural_from_internet.autonomous_steering_logic2 import AutonomousSteeringLogic2
import math

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.autonomous_steering_logic = AutonomousSteeringLogic()
    self.chromosome_helper = ChromosomeHelper()
    self.chromosome = []
    self.fitness = None

  def set_chromosome(self, chromosome):
    self.chromosome = chromosome
    weights = self.chromosome_helper.genome_to_decimals(self.chromosome)
    if self.autonomous_steering_logic.number_of_network_weights() != len(weights):
      raise Exception("Invalid number of weights in chromosome")

    self.autonomous_steering_logic.set_neural_weights(weights)

  def reset(self, pos_x, pos_y):
    self.init_moving(pos_x, pos_y)
    self.alive = True

  def get_steering_dict(self):
    sensors_input = [s['sensor'].actual_length_in_meter() for s in self.sensors]
    return self.autonomous_steering_logic.get_steering_dict(sensors_input)
    # return ControlledCar.get_steering_dict(self)
