
import pygame
import os
from car import Car
from car import *
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

    self.level = Level({'path': 'map/road.csv'})
    for o in self.level.level_objects:
      self.all_sprites.add(o)
    self.add_car(ControllerCar(Car.HEIGHT/2, screen_height - Car.HEIGHT - 40))
    self.add_cars_with_slot()

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

  def add_cars_with_slot(self):
    # Empty space between cars
    empty_space = 0
    for car_number in range(9):
      # Add upper cars
      self.add_car(NotSteerableCar(Car.HEIGHT/2 + Car.HEIGHT * car_number + empty_space, screen_height - Car.HEIGHT*2 - 20))
      if car_number == 3:
        empty_space += 50
        continue
      # Add cars at the bottom with empty parks slot
      self.add_car(NotSteerableCar(Car.HEIGHT/2 + Car.HEIGHT * car_number + empty_space, screen_height - Car.HEIGHT / 2))
      empty_space += 20


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
