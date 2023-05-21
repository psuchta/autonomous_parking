import pygame
from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.controlled_car import ControlledCar
import math
import numpy as np
from world.settings import meter_scale

class DeepControlledCar(AutonomousControlledCar):
  def __init__(self, pos_x, pos_y, screen, game):
    AutonomousControlledCar.__init__(self, pos_x, pos_y, screen, game)
    self.parking_spot = None
    self.next_action = None

  def init_constants(self):
    AutonomousControlledCar.init_constants(self)
    # self.max_velocity = 1.7

  def set_parking_spot(self, parking_spot):
    self.parking_spot = parking_spot

  # add aditional inputs - distance between parkink slot and car position
  def get_sensors_data(self):
    if self.parking_spot == None:
      raise Exception("You have to set parking spot")

    inputs = [np.interp(s['sensor'].actual_length , [0, s['sensor'].max_length], [-1, 1]) for s in self.sensors]
    pivot = self.rect.center
    car_coordiantes = self.original.get_rect(center = pivot).center
    parking_coordinates = self.parking_spot.rect.center
    relative_x = car_coordiantes[0] - parking_coordinates[0]
    relative_y = parking_coordinates[1] - car_coordiantes[1]

    inputs.append(np.interp(relative_x, [-200, 700], [-1, 1]))
    inputs.append(np.interp(relative_y, [-20, 157], [-1, 1]))
    inputs.append(np.interp(self.angle % 360, [0, 360], [-1, 1]))

    return inputs

  def set_next_action(self, action):
    self.next_action = action

  def get_steering_dict(self):
    return self.map_steering(self.next_action)

  # def get_steering_dict(self):
    # return ControlledCar.get_steering_dict(self)

  def distance_to_parking(self, parking_spot):
    distances = []
    pivot = self.rect.center
    rect = self.original.get_rect(center = pivot)

    pts = [rect.center]
    # pts = [rect.bottomleft]
    pts = [(pygame.math.Vector2(p) - pivot).rotate(-self.angle) + pivot for p in pts]
    parking_point = (parking_spot.rect.midright[0]-40, parking_spot.rect.midright[1])
    
    distances.append(self.distance_between_points(pts[0], parking_spot.rect.center))
    distance = distances[0]/meter_scale
    # TODO TUTAJ DAC SAMO sum(distances)
    return distance

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
