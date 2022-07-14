import pygame
import math
import numpy as np
# https://stackoverflow.com/questions/34456195/make-a-line-as-a-sprite-with-its-own-collision-in-pygame/65324946#65324946
class Sensor:
  def __init__(self, game, screen, initial_angle):
    pygame.sprite.Sprite.__init__(self)
    self.sensor_length = 40
    self.initial_angle = initial_angle
    self.game = game
    self.screen = screen

  def get_not_steerable(self):
    return self.game.not_steerable_cars

  def update(self, sensor_position, angle):
    # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
    # print(car.mask.get_at((10,10)))
    # print(car.rect.x)
    angle = self.initial_angle + angle
    length = 0
    touching = False
    x, y = None, None
    while length < self.sensor_length and (touching == False):
        length += 1
        x = sensor_position[0] + math.cos(math.radians(-angle)) * length
        y = sensor_position[1] + math.sin(math.radians(-angle)) * length
        for c in self.get_not_steerable():
          pos_in_mask = x - c.rect.x, y - c.rect.y
          touching = c.rect.collidepoint((x,y)) and c.mask.get_at(pos_in_mask)
          if(touching):
            break
    pygame.draw.line(self.screen, (255, 255, 255), sensor_position, (x, y), 1)