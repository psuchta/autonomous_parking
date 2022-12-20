from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.steering_logic.deep_steering_logic import DeepSteeringLogic
import math

class DeepControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.set_steering_logic(DeepSteeringLogic())
