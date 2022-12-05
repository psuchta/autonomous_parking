from cars.autonomous_controlled_car import AutonomousControlledCar
from base_program import BaseProgram
import numpy as np
import pygame
import random
import neat

class NeatProgram(BaseProgram):
  def __init__(self):
    BaseProgram.__init__(self)

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    car = AutonomousControlledCar(700, 430, self.screen, self)
    self.add_car(car)
