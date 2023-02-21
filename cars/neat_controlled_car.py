from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.steering_logic.neat_steering_logic import NeatSteeringLogic
import math

class NeatControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.set_steering_logic(NeatSteeringLogic())

  def init_constants(self):
    AutonomousControlledCar.init_constants(self)
    self.max_velocity = 1.7

  def set_chromosome(self, chromosome, config):
    AutonomousControlledCar.set_chromosome(self, chromosome)
    self.autonomous_steering_logic.set_neural_weights(chromosome, config)
