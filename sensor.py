import pygame
import math
# https://stackoverflow.com/questions/34456195/make-a-line-as-a-sprite-with-its-own-collision-in-pygame/65324946#65324946
class Sensor(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.sensor_length = 150
    self.image = pygame.Surface([self.sensor_length, self.sensor_length], pygame.SRCALPHA)
    # self.image.set_colorkey((0, 0, 0))
    self.rect = self.image.get_rect(center = (0, 0))
    self.mask = pygame.mask.from_surface(self.image)
    
  def update(self, car, car_coordinates,screen):
    self.rect = self.image.get_rect(center = car_coordinates)
    x = car_coordinates[0] + math.cos(math.radians(0)) * self.sensor_length
    y = car_coordinates[1] + math.sin(math.radians(0)) * self.sensor_length
    col = pygame.sprite.collide_mask(car, self)
    print(car_coordinates)
    print('xy')
    print((x,y))
    # print(col)
    # if col == True:
    #   self.image.fill(255)
    # else:
    #   self.image.fill(1)
    # pygame.draw.line(self.image, (255, 255, 255), (car_coordinates[0], car_coordinates[1] ), (x, y), 1)
    pygame.draw.line(screen, (255, 255, 255), car_coordinates, (x, y), 1)
    self.mask = pygame.mask.from_surface(self.image)

    # radar = self.rect.center
    # radar_len = 200
    
    # x = radar[0] + math.cos(math.radians(20)) * radar_len
    # y = radar[1] + math.sin(math.radians(20)) * radar_len