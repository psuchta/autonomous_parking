import pygame
import math
# https://stackoverflow.com/questions/34456195/make-a-line-as-a-sprite-with-its-own-collision-in-pygame/65324946#65324946
class Sensor:
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.sensor_length = 150

  def update(self, car, car_coordinates,screen, angle):
    # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
    # print(car.mask.get_at((10,10)))
    print(car.rect.x)
    x = car_coordinates[0] + math.cos(math.radians(-angle)) * self.sensor_length
    y = car_coordinates[1] + math.sin(math.radians(-angle)) * self.sensor_length
    # print(col)
    # if col == True:
    #   self.image.fill(255)
    # else:
    #   self.image.fill(1)
    # pygame.draw.line(self.image, (255, 255, 255), (car_coordinates[0], car_coordinates[1] ), (x, y), 1)
    pygame.draw.line(screen, (255, 255, 255), car_coordinates, (x, y), 1)

    # radar = self.rect.center
    # radar_len = 200
    
    # x = radar[0] + math.cos(math.radians(20)) * radar_len
    # y = radar[1] + math.sin(math.radians(20)) * radar_len