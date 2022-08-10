import pygame

class ParkingSlot(pygame.sprite.Sprite):
  RED = (255,0,0)

  def __init__(self, position, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
    self.image = self.image.convert_alpha()
    pygame.draw.rect(self.image,
                     self.RED,
                     pygame.Rect(0, 0, width, height), 2)
    self.rect = self.image.get_rect(topleft = position)

  # Function result is not precise, it should only be an approximation
  # Alternatively
  # https://stackoverflow.com/questions/44797713/calculate-the-area-of-intersection-of-two-rotated-rectangles-in-python
  def car_intersection_ratio(self, car_rectangle):
    intersection_rect = pygame.Rect.clip(self.rect, car_rectangle)
    car_surface = car_rectangle.width * car_rectangle.height
    intersection_area = intersection_rect.width * intersection_rect.height
    return intersection_area/car_surface
