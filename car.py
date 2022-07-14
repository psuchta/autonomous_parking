# Trygonometry
# https://www.youtube.com/watch?v=SEqFQl2ADi0

import pygame
import os
from math import pi, sin, cos, tan, radians, degrees, copysign
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from sensor import Sensor
import math
import numpy as np

from fuzzy_steering import FuzzySteering

class Car(pygame.sprite.Sprite):
  HEIGHT = 128
  WIDTH = 64
  METER_SCALE = 32

  # Center of a Car will be positioned to the given coordinates
  def __init__(self, pos_x, pos_y, game):
    pygame.sprite.Sprite.__init__(self)
    self.original = pygame.image.load('assets/car.png').convert_alpha()
    self.image = self.original
    self.rect = self.image.get_rect()
    self.rect.center = [pos_x, pos_y]
    self.walls = None
    self.init_moving(pos_x, pos_y)
    self.game = game
    self.mask = pygame.mask.from_surface(self.image)

  def get_all_sprites(self):
    return []

  def init_moving(self, x, y, angle=0.0, length=2, max_steering=45, max_acceleration=3.0):
    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0.0, 0.0)
    self.angle = angle
    self.length = length
    self.max_acceleration = max_acceleration
    self.max_steering = max_steering
    self.init_constants()

  def init_constants(self):
    self.acceleration = 0.0
    self.steering = 0.0
    self.free_deceleration = 10
    self.max_velocity = 5
    self.brake_deceleration = 15

  def update(self, dt = 0):
    self.velocity += (self.acceleration * dt, 0)
    self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

    if self.steering:
      turning_radius = self.length / sin(radians(self.steering))
      # https://www.youtube.com/watch?v=QnXxdIP3U-Q
      angular_velocity = self.velocity.x / turning_radius
    else:
      angular_velocity = 0

    # All the move constants are in meter units. We have to scale meters to pixels
    self.position += self.velocity.rotate(-self.angle) * dt * self.METER_SCALE
    self.angle += degrees(angular_velocity) * dt
    self.rect.center = self.position

    ######## OLD STEERING MODEL ############
    # calculate values which will shift actual position of the car
    # x_change, y_change = self.update_position()
    # self.position.x += self.scale_position_change(x_change, dt)
    # self.position.y -= self.scale_position_change(y_change, dt)
    # self.rect.center = self.position
    # self.check_collision()
    self.rotate()

  def rotate(self):
    c = self.rect.center
    # Usage of rotozoom giving better rotation quality than rotate method
    self.image = pygame.transform.rotozoom(self.original, self.angle, 1)
    self.rect = self.image.get_rect(center = c)
    self.mask = pygame.mask.from_surface(self.image)


  def update_position(self):
    x_change = self.velocity.x * cos(radians(self.angle)) * cos(radians(self.steering))
    y_change = self.velocity.x * sin(radians(self.angle)) * cos(radians(self.steering))
    self.angle += degrees(self.velocity.x / self.length * sin(radians(self.steering)))
    return x_change, y_change
  
  # Multiply change vector by delta time between each frame, 32 is one meter in real world  
  def scale_position_change(self, point, dt):
    return point * dt * self.WIDTH / 2

  def check_collision(self):

    blocking_cars = pygame.sprite.spritecollide(self, self.walls, False, pygame.sprite.collide_mask)
    if len(blocking_cars) > 1:

      # print('first collide', len(blocking_walls))
      # self.position.x += self.scale_position_change(-copysign(10, x_change), dt)
      # self.position.y -= self.scale_position_change(-copysign(10, y_change), dt)
      # self.rect.center = self.position
      self.velocity.x = 0

class ControllerCar(Car):
  def __init__(self, pos_x, pos_y, screen, game):
    Car.__init__(self, pos_x, pos_y, game)
    self.screen = screen
    self.max_steering = 25
    self.key_mapping = {
      'up': pygame.K_UP,
      'down': pygame.K_DOWN,
      'brake': pygame.K_SPACE,
      'right': pygame.K_RIGHT,
      'left': pygame.K_LEFT
    }
    self.init_sensors()

  def update(self, dt):
    self.detect_steering(dt)
    super().update(dt)
    # sensor_coordiantes = tuple(np.add(self.rect.center,(WIDTH/2,HEIGHT/2)))
    for s in self.sensors:
      shift_angle = s['shift_position']
      sensor_position = self.compute_sensor_position(self.rect.center, shift_angle['angle'], shift_angle['length'])
      sensor = s['sensor']
      sensor.update(sensor_position, self.angle)

  def init_sensors(self):
    self.sensors = []
    # Left Front
    s = Sensor(self.game, self.screen, 90)
    shift_position = {'angle': 50, 'length': 39}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Left rear
    s = Sensor(self.game, self.screen, 90)
    shift_position = {'angle': 140, 'length': 45}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})

    # Rear right
    s = Sensor(self.game, self.screen, 135)
    shift_position = {'angle': 160, 'length': 66}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Rear middle
    s = Sensor(self.game, self.screen, 180)
    shift_position = {'angle': 180, 'length': 66}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Rear right
    s = Sensor(self.game, self.screen, 225)
    shift_position = {'angle': 200, 'length': 66}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})

    # Right Front
    s = Sensor(self.game, self.screen, 270)
    shift_position = {'angle': -50, 'length': 39}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Right rear
    s = Sensor(self.game, self.screen, 270)
    shift_position = {'angle': -140, 'length': 45}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})


    # Rear right
    s = Sensor(self.game, self.screen, 45)
    shift_position = {'angle': 20, 'length': 63}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Rear middle
    s = Sensor(self.game, self.screen, 0)
    shift_position = {'angle': 0, 'length': 66}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Rear right
    s = Sensor(self.game, self.screen, -45)
    shift_position = {'angle': -20, 'length': 63}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})


  def detect_steering(self, dt):
    pressed = pygame.key.get_pressed()
    loc_max_acceleration = self.max_acceleration

    if pressed[self.key_mapping['up']]:
      if self.velocity.x < 0:
        self.acceleration = loc_max_acceleration = self.brake_deceleration
      else:
        self.acceleration += 1 * dt
    elif pressed[self.key_mapping['down']]:
      if self.velocity.x > 0:
        self.acceleration =  -self.brake_deceleration
        loc_max_acceleration = self.brake_deceleration
      else:
        self.acceleration -= 1 * dt
    elif pressed[self.key_mapping['brake']]:
      if abs(self.velocity.x) > dt * self.brake_deceleration:
        self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
      else:
        self.acceleration = -self.velocity.x / dt
    else:
      if abs(self.velocity.x) > dt * self.free_deceleration:
        self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
      else:
        if dt != 0:
          self.acceleration = -self.velocity.x / dt
    self.acceleration = max(-loc_max_acceleration, min(self.acceleration, loc_max_acceleration))

    if pressed[self.key_mapping['right']]:
      if self.steering > 0:
        steering_add = 90
      else:
        steering_add = 30
      self.steering -= steering_add * dt
    elif pressed[self.key_mapping['left']]:
      if self.steering < 0:
        steering_add = 90
      else:
        steering_add = 30
      self.steering += steering_add * dt
    else:
      self.steering = 0
    self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

  def compute_sensor_position(self, car_coordinates, sensor_angle, sensor_init_length):
    sensor_angle += self.angle
    sensor_coordiantes = tuple(np.add(car_coordinates,(0,20.0)))
    x = car_coordinates[0] + math.cos(math.radians(-sensor_angle)) * sensor_init_length
    y = car_coordinates[1] + math.sin(math.radians(-sensor_angle)) * sensor_init_length
    return x,y


class AutonomousCar(Car):
  def __init__(self, pos_x, pos_y, game):
    Car.__init__(self, pos_x, pos_y, game)
    self.velocity = pygame.Vector2(-5.0, 0.0)
    self.fuzzy_steering = FuzzySteering()

  def autonomouse_steering(self, dt, parking_slot):
    parking_x_beginning = parking_slot.slot_x - parking_slot.slot_width/2
    parking_width = parking_x_beginning + parking_slot.slot_width
    parking_height = parking_slot.slot_height

    xa = (self.position.x - parking_x_beginning) / (parking_slot.slot_width)
    xy = self.position.y / parking_height
    self.update(dt)
    self.steering = self.fuzzy_steering.get_steering(xa , xy, self.angle)

class NotSteerableCar(Car):
  def update(self, dt):
    return


