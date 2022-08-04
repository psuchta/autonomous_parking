# Trygonometry
# https://www.youtube.com/watch?v=SEqFQl2ADi0

import pygame
import os
from math import sin, cos, radians, degrees
import numpy as np
from sensor import Sensor
from world.settings import meter_scale

class Car(pygame.sprite.Sprite):
  HEIGHT = 128
  WIDTH = 64

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
    self.alive = True

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
    self.move_itself(dt)

  def move_itself(self, dt = 0):
    self.velocity += (self.acceleration * dt, 0)
    self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

    if self.steering:
      turning_radius = self.length / sin(radians(self.steering))
      # https://www.youtube.com/watch?v=QnXxdIP3U-Q
      angular_velocity = self.velocity.x / turning_radius
    else:
      angular_velocity = 0

    # All the move constants are in meter units. We have to scale meters to pixels
    self.position += self.velocity.rotate(-self.angle) * dt * meter_scale
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
      self.velocity.x = 0
