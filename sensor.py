import pygame
import math
import numpy as np
from settings import meter_scale
# https://stackoverflow.com/questions/34456195/make-a-line-as-a-sprite-with-its-own-collision-in-pygame/65324946#65324946
class Sensor:
  def __init__(self, game, screen, initial_angle):
    pygame.sprite.Sprite.__init__(self)
    self.max_length = 96
    self.actual_length = 0
    self.initial_angle = initial_angle
    self.game = game
    self.screen = screen

  def get_not_steerable(self):
    return self.game.not_steerable_cars

  def actual_length_in_meter(self):
    return self.actual_length / meter_scale

  def update(self, sensor_position, angle):
    # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
    # print(car.mask.get_at((10,10)))
    # print(car.rect.x)
    angle = self.initial_angle + angle
    self.actual_length = 0
    touching = False
    x, y = None, None
    while self.actual_length < self.max_length and (touching == False):
        self.actual_length += 1
        x = sensor_position[0] + math.cos(math.radians(-angle)) * self.actual_length
        y = sensor_position[1] + math.sin(math.radians(-angle)) * self.actual_length
        for c in self.get_not_steerable():
          pos_in_mask = x - c.rect.x, y - c.rect.y
          touching = c.rect.collidepoint((x,y)) and c.mask.get_at(pos_in_mask)
          if(touching):
            break
    pygame.draw.line(self.screen, (255, 255, 255), sensor_position, (x, y), 1)