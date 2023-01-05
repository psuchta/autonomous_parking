from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.steering_logic.deep_steering_logic import DeepSteeringLogic
import math

class DeepControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.parking_spot = None
    # self.set_steering_logic(DeepSteeringLogic())

  def set_parking_spot(self, parking_spot):
    self.parking_spot = parking_spot

  # add aditional inputs - distance between parkink slot and car position
  def get_sensors_data(self):
    if self.parking_spot == None:
      raise Exception("You have to set parking spot")

    inputs = [s['sensor'].actual_length_in_meter() for s in self.sensors]
    ditance = self.distance_between_points(self.parking_spot.rect.center, self.rect.center)
    inputs.append(ditance)
    return inputs
