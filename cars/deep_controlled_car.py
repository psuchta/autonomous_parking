from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.steering_logic.deep_steering_logic import DeepSteeringLogic
from cars.controlled_car import ControlledCar
import math

class DeepControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.parking_spot = None
    self.next_action = None

  def set_parking_spot(self, parking_spot):
    self.parking_spot = parking_spot

  # add aditional inputs - distance between parkink slot and car position
  def get_sensors_data(self):
    if self.parking_spot == None:
      raise Exception("You have to set parking spot")

    inputs = [s['sensor'].actual_length for s in self.sensors]
    # inputs.extend(self.parking_spot.rect.center)
    # inputs.extend(self.rect.center)
    ditance = self.distance_between_points(self.parking_spot.rect.center, self.rect.center)
    inputs.append(ditance)
    return inputs

  def set_next_action(self, action):
    self.next_action = action

  def get_steering_dict(self):
    return self.map_steering(self.next_action)

  # def get_steering_dict(self):
    # return ControlledCar.get_steering_dict(self)


  def map_steering(self, action):
    up = action == 0
    down = action == 1
    upleft = action == 2
    upright = action == 3
    downleft = action == 4
    downright = action == 5

    steering_dict = {
      'up': False,
      'down': False,
      'brake': False,
      'right': False,
      'left': False
    }

    if up == True:
      steering_dict['up'] = True
    if down == True:
      steering_dict['down'] = True

    if upleft == True:
      steering_dict['up'] = True
      steering_dict['left'] = True
    if upright == True:
      steering_dict['up'] = True
      steering_dict['right'] = True

    if downleft == True:
      steering_dict['down'] = True
      steering_dict['left'] = True
    if downright == True:
      steering_dict['down'] = True
      steering_dict['right'] = True
    return steering_dict