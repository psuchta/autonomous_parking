from cars.controlled_car import ControlledCar
from genome_helper import GenomeHelper
from autonomous_steering_logic import AutonomousSteeringLogic

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.autonomous_steering_logic = AutonomousSteeringLogic()
    self.genome = []

  def set_genome(self, genome):
    self.genome = genome

  def reset(self, pos_x, pos_y):
    self.init_moving(pos_x, pos_y)
    self.alive = True

  def get_steering_dict(self):
    sensors_input = [s['sensor'].actual_length_in_meter() for s in self.sensors]
    return self.autonomous_steering_logic.get_steering_dict(self.genome, sensors_input)
    # return ControlledCar.get_steering_dict(self)
