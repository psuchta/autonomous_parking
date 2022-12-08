from cars.controlled_car import ControlledCar
import math

class AutonomousControlledCar(ControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    ControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.autonomous_steering_logic = None
    self.chromosome = []
    self.fitness = None

  def set_steering_logic(self, steering_logic):
    self.autonomous_steering_logic = steering_logic

  def set_chromosome(self, chromosome):
    self.chromosome = chromosome

  def reset(self, pos_x, pos_y):
    self.init_moving(pos_x, pos_y)
    self.alive = True

  def get_steering_dict(self):
    sensors_input = [s['sensor'].actual_length_in_meter() for s in self.sensors]
    return self.autonomous_steering_logic.get_steering_dict(sensors_input)
    # return ControlledCar.get_steering_dict(self)
