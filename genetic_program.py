from base_program import BaseProgram
from genetic_helper import GeneticHelper
import pygame

class GeneticProgram(BaseProgram):
  def __init__(self):
    BaseProgram.__init__(self)
    self.genetic_helper = GeneticHelper()

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def run_generation(self, gen_num):
    time_passed = 0
    start_time = pygame.time.get_ticks()
    while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 7000:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.draw_objects(dt)
      self.draw_generation_num(gen_num)
      pygame.display.flip()
      self.clock.tick(self.fps)
      time_passed = pygame.time.get_ticks() - start_time


  def run(self):
    generation_size = 3
    for g in range(generation_size):
      if self.exit: break

      self.run_generation(g)
      [car.reset(64, 408) for car in self.steerable_cars]
    pygame.quit()
