from base_program import BaseProgram
from cars.deep_controlled_car import DeepControlledCar
import pygame
import random
import numpy as np

MAX_MEMORY = 1000000
BATCH_SIZE = 64
LR = 0.00025
GAMMA = 0.9

class ReinforcementProgram(BaseProgram):
  def __init__(self):
    BaseProgram.__init__(self)
    self.autonomous_car = self.steerable_cars[0]
    self.n_games = 0
    self.previous_reward = 0
    self.fps = 30
    self.best_intersection_ratio = 0

  def reset(self):
    self.n_games += 1
    random_coordinates = self.get_random_location()
    [car.reset(random_coordinates[0], random_coordinates[1]) for car in self.steerable_cars]
    # [car.reset(400, 430) for car in self.steerable_cars]
    # Change in future
    self.previous_reward = 10.394337319652962
    self.best_intersection_ratio = 0
    observation = self.get_state()
    observation = np.array(observation)

    return observation

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)

    car = DeepControlledCar(*self.get_random_location(), self.screen, self)
    self.add_car(car)
    car.set_parking_spot(self.parking_slot)

  def get_state(self):
    state = self.autonomous_car.get_sensors_data()
    return np.array(state, dtype=float)

  # NOT USED penalty for each step, if car is closer to parking spot the penalty is lower
  def get_fitness(self, car, parking_spot):
    distance_loss = car.distance_to_parking(parking_spot)/22
      
    fitness = 1/(distance_loss+1)
    # car.fitness = fitness
    return -distance_loss

  def fitness_step(self, car, parking_spot):
    distance_to_parking = car.distance_to_parking(parking_spot)
    reward = 22 - distance_to_parking
    return reward

  def play_step(self, delta_time):
    self.draw_objects(delta_time)
    self.draw_generation_num()
    # current_fitness = self.get_fitness(self.autonomous_car, self.parking_slot)
    # reward = current_fitness
    # reward = self.fitness(self.autonomous_car, self.parking_slot)
    current_reward = self.fitness_step(self.autonomous_car, self.parking_slot)
    reward = current_reward - self.previous_reward
    intersection_ratio = self.parking_slot.car_intersection_ratio(self.autonomous_car.rect)

    if intersection_ratio:
      reward = 0
    
    if intersection_ratio > self.best_intersection_ratio:
      reward = 0.1
      self.best_intersection_ratio = intersection_ratio
    if(intersection_ratio > 0.70):
      reward = 1

    self.previous_reward = current_reward
    # Did car hit something
    is_done = (not self.autonomous_car.alive)
    if is_done:
      self.previous_reward = 0
      reward = -1
    return reward, is_done

  def draw_generation_num(self):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(self.n_games), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def step(self, action):
    self.autonomous_car.set_next_action(action)
    # dt = self.clock.get_time() / 1000
    dt = 0.033
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.exit = True

    reward, is_done = self.play_step(dt)
    last_action = [0,0,0,0,1,0]
    observation = self.get_state()

    pygame.display.flip()
    self.clock.tick(self.fps)

    info = {}
    observation = np.array(observation)
    return observation, reward, is_done, info

  def can_close(self):
    return self.exit

  def close(self):
    pygame.quit()

  def get_random_location(self):
    return 700, 430
