from cars.controlled_car import ControlledCar
from genome_helper import GenomeHelper
from autonomous_steering_logic import AutonomousSteeringLogic
import math

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.autonomous_steering_logic = AutonomousSteeringLogic()
    self.genome_helper = GenomeHelper()
    self.genome = []

  def set_genome(self, genome):
    self.genome = genome
    coefficients = self.genome_helper.genome_to_decimals(self.genome)
    engine_signal, wheels_signal = self.genome_helper.engine_wheels_signal(coefficients)
    self.engine_signal = engine_signal
    self.wheels_signal = wheels_signal

  def reset(self, pos_x, pos_y):
    self.init_moving(pos_x, pos_y)
    self.alive = True

  def get_steering_dict(self):
    sensors_input = [s['sensor'].actual_length_in_meter() for s in self.sensors]
    return self.autonomous_steering_logic.get_steering_dict(self.engine_signal, self.wheels_signal, sensors_input)
    # return ControlledCar.get_steering_dict(self)
