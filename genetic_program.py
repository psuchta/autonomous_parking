from base_program import BaseProgram
import pygame

class GeneticProgram(BaseProgram):
  def run_generation(self):
    time_passed = 0
    start_time = pygame.time.get_ticks()
    while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 13000:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.draw_objects(dt)
      pygame.display.flip()
      self.clock.tick(self.fps)
      time_passed = pygame.time.get_ticks() - start_time


  def run(self):
    generation_size = 3
    for g in range(generation_size):
      if self.exit: break

      self.run_generation()
      [car.reset(64, 408) for car in self.steerable_cars]
    pygame.quit()
