from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.steering_logic.deep_steering_logic import DeepSteeringLogic
import math

class DeepControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.set_steering_logic(DeepSteeringLogic())

  def get_steering_action(self):
    sensors_input = self.get_sensors_data()
    return self.autonomous_steering_logic.get_steering_action(sensors_input)
