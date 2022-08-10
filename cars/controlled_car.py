import pygame
import os
from math import sin, cos, radians, copysign
import numpy as np
from sensor import Sensor
from world.settings import meter_scale
from cars.car import Car

class ControlledCar(Car):
  CAR_SENSORS_NUM = 10

  def __init__(self, pos_x, pos_y, screen, game):
    Car.__init__(self, pos_x, pos_y, game)
    self.screen = screen
    self.max_steering = 30
    self.key_mapping = {
      'up': pygame.K_UP,
      'down': pygame.K_DOWN,
      'brake': pygame.K_SPACE,
      'right': pygame.K_RIGHT,
      'left': pygame.K_LEFT
    }
    self.init_sensors()

  def get_steering_dict(self):
    pressed = pygame.key.get_pressed()
    steering_dict = {}
    # Create dictionary with boolean values. 
    # When key from key_mapping is pressed, its value is set to True
    for key in self.key_mapping.keys():
      steering_dict[key] = pressed[self.key_mapping[key]]
    return steering_dict

  def update(self, dt):
    if not self.alive:
      return

    steering_dict = self.get_steering_dict()
    self.update_steer(dt, steering_dict)
    super().update(dt)
    for s in self.sensors:
      shift_angle = s['shift_position']
      sensor_position = self.compute_sensor_position(self.rect.center, shift_angle['angle'], shift_angle['length'])
      sensor = s['sensor']
      sensor.update(sensor_position, self.angle)
    self.check_if_hit_something()

  def update_steer(self, dt, steering_dict):
    loc_max_acceleration = self.max_acceleration

    if steering_dict['up']:
      if self.velocity.x < 0:
        self.acceleration = loc_max_acceleration = self.brake_deceleration
      else:
        self.acceleration += 1 * dt
    elif steering_dict['down']:
      if self.velocity.x > 0:
        self.acceleration =  -self.brake_deceleration
        loc_max_acceleration = self.brake_deceleration
      else:
        self.acceleration -= 1 * dt
    elif steering_dict['brake']:
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

    if steering_dict['right']:
      if self.steering > 0:
        self.steering = 0
      else:
        self.steering -= 30 * dt
    elif steering_dict['left']:
      if self.steering < 0:
        self.steering = 0
      else:
        self.steering += 30 * dt
    else:
      self.steering = 0
    self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

  def compute_sensor_position(self, car_coordinates, sensor_angle, sensor_init_length):
    sensor_angle += self.angle
    sensor_coordiantes = tuple(np.add(car_coordinates,(0,20.0)))
    x = car_coordinates[0] + cos(radians(-sensor_angle)) * sensor_init_length
    y = car_coordinates[1] + sin(radians(-sensor_angle)) * sensor_init_length
    return x,y

  def init_sensors(self):
    # TODO simplify this method
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


    # Front right
    s = Sensor(self.game, self.screen, 45)
    shift_position = {'angle': 20, 'length': 63}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Front middle
    s = Sensor(self.game, self.screen, 0)
    shift_position = {'angle': 0, 'length': 66}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})
    # Front right
    s = Sensor(self.game, self.screen, -45)
    shift_position = {'angle': -20, 'length': 63}
    self.sensors.append({'sensor': s, 'shift_position': shift_position})

  def check_if_hit_something(self):
    self.alive = all(not s['sensor'].hit_something() for s in self.sensors)
