
import pygame
import os
from car import Car
from car import AutonomousCar
from car import ControllerCar
from wall import Wall
from wall import ParkingSlot
from math import copysign
from settings import *
from level import Level


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class Game:
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Car parking with fuzzy sets')
    self.screen = pygame.display.set_mode((screen_width, screen_height))
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.__add_game_objects()
    self.exit = False

  def draw_objects(self):
    self.screen.fill(self.WHITE)
    self.all_sprites.draw(self.screen)
    pygame.display.update()

  def __add_game_objects(self):
    self.all_sprites = pygame.sprite.Group()
    self.cars = []
    self.walls = pygame.sprite.Group()
    # self.add_car(AutonomousCar(600, 240 + 64))

    # Create walls starting from 0 (x) 140 (y)
    # Center of the parking slot is 40(x)
    # Slot width is 80 px
    # Slot height is 140 px

    # self.parking_slot = ParkingSlot(0, 140, 140, 80, 140)
    # for w in self.parking_slot.walls:
    #   self.all_sprites.add(w)
    #   self.walls.add(w)

    self.level = Level({'path': 'map/parking1.csv'})
    for o in self.level.level_objects:
      self.all_sprites.add(o)
    self.add_car(ControllerCar(400, 140 + 64))

  def add_car(self, car):
    self.cars.append(car)
    self.all_sprites.add(car)
    car.walls = self.all_sprites

  def update_cars(self, cars, dt):
    for car in cars:
      if isinstance(car, AutonomousCar): 
        car.autonomouse_steering(dt)
      else:
        car.update(dt)


  def run(self):
    while not self.exit:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.update_cars(self.cars, dt)
      self.draw_objects()
      self.clock.tick(self.fps)
    pygame.quit()

if __name__ == '__main__':
  game = Game()
  game.run()
