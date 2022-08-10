import pygame

class Wall(pygame.sprite.Sprite):
  BLACK = (0,0,0)
  def __init__(self, x, y, width = 2, height = 2):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([width, height])
    self.image.fill(self.BLACK)
    self.rect = self.image.get_rect()
    self.rect.y = y
    self.rect.x = x
    self.mask = pygame.mask.from_surface(self.image)