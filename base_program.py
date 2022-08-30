
import pygame
import os
from cars.autonomous_controlled_car import AutonomousControlledCar
from cars.not_steerable_car import NotSteerableCar
from parking_slot import ParkingSlot
from world.settings import *
from world.level import Level
from cars.car import Car
from cars.controlled_car import ControlledCar
from world.wall import Wall

import numpy as np

class BaseProgram:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Car parking with fuzzy sets')
    self.screen = pygame.display.set_mode((screen_width, screen_height))
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.add_game_objects()
    self.exit = False

  def draw_objects(self, dt):
    self.world_sprites.draw(self.screen)
    self.update_cars(self.cars, dt)
    self.cars.draw(self.screen)

  def add_game_objects(self):
    self.parking_slot = ParkingSlot((458, 480), 128, 64)
    self.world_sprites = pygame.sprite.Group()
    self.cars = pygame.sprite.Group()
    self.collision_objects = []
    self.steerable_cars = []
    # self.add_car(AutonomousCar(600, 240 + 64))

    self.level = Level({'path': 'world/road.csv'})
    for o in self.level.level_objects:
      self.world_sprites.add(o)

    self.world_sprites.add(self.parking_slot)
    walls = [
      [0, 560, screen_width, 20],
      [screen_width, 0, 20, screen_height],
      [-20, 0, 20, screen_height],
    ]

    for wall in walls:
      wall = Wall(wall[0], wall[1], wall[2], wall[3])
      self.collision_objects.append(wall)
      self.world_sprites.add(wall)

    self.add_cars_with_slot()

  def add_car(self, car, not_steerable=False):
    if not_steerable: 
      self.collision_objects.append(car)
    else:
      self.steerable_cars.append(car)
    self.cars.add(car)
    self.world_sprites.add(car)

  def update_cars(self, cars, dt):
    for car in cars:
      car.update(dt)

  def add_cars_with_slot(self):
    # Empty space between cars
    empty_space = 0
    for car_number in range(9):
      # Add upper cars
      self.add_car(NotSteerableCar(NotSteerableCar.HEIGHT/2 + NotSteerableCar.HEIGHT * car_number + empty_space, screen_height - NotSteerableCar.HEIGHT*2 - 20, self), True)
      if car_number == 3:
        empty_space += 50
        continue
      # Add cars at the bottom with empty parks slot
      self.add_car(NotSteerableCar(NotSteerableCar.HEIGHT/2 + NotSteerableCar.HEIGHT * car_number + empty_space, screen_height - NotSteerableCar.HEIGHT / 2, self), True)
      empty_space += 20


  def run(self):
    while not self.exit:
      dt = self.clock.get_time() / 1000
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.exit = True      
      self.draw_objects(dt)
      pygame.display.flip()
      self.clock.tick(self.fps)
    pygame.quit()
