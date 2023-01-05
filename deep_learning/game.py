from base_program import BaseProgram
from cars.deep_controlled_car import DeepControlledCar
from collections import deque
import pygame
import random
import numpy as np

MAX_MEMORY = 1000000
BATCH_SIZE = 64
LR = 0.00025
GAMMA = 0.9

class Game(BaseProgram):
  def __init__(self):
    BaseProgram.__init__(self)
    self.autonomous_car = self.steerable_cars[0]
    # self.car_steering_model = self.autonomous_car.autonomous_steering_logic.neural_network
    # self.car_steering_logic = self.autonomous_car.autonomous_steering_logic

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    car = DeepControlledCar(700, 430, self.screen, self)
    self.add_car(car)
    car.set_parking_spot(self.parking_slot)

  def get_state(self):
    state = self.autonomous_car.get_sensors_data()
    return np.array(state, dtype=float)

  # penalty for each step, if car is closer to parking spot the penalty is lower
  def get_fitness(self, car, parking_spot):
    distance_loss = car.distance_to_parking(parking_spot)/22
      
    fitness = 1/(distance_loss+1)
    # car.fitness = fitness
    return -distance_loss

  def play_step(self, n_games, delta_time):
    self.draw_objects(delta_time)
    self.draw_generation_num(n_games)
    current_fitness = self.get_fitness(self.autonomous_car, self.parking_slot)
    # print(current_fitness)
    delta_fintness = current_fitness - self.previous_fitness
    reward = current_fitness
    # if delta_fintness < 0:
    #   reward = -2
    # elif delta_fintness > 0:
    #   reward = 1
    # print(reward)
    self.previous_fitness = current_fitness
    # Did car hit something
    is_done = not self.autonomous_car.alive
    if is_done:
      reward = -100

    self.total_steps += 1
    return reward, is_done

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def train(self, n_games, dt):
    state_old = self.get_state()
    reward, is_done = self.play_step(n_games, dt)
    last_action = [0,0,0,0,1,0]
    state_new = self.get_state()

    loss = None
    return (reward, loss)


  def run(self):
    n_games = 0
    self.total_steps = 0
    while not self.exit:
      start_time = pygame.time.get_ticks()
      time_passed = 0
      self.previous_fitness = 0
      while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 10000:
        dt = self.clock.get_time() / 1000
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.exit = True      
        reward, short_loss = self.train(n_games, dt)
        pygame.display.flip()
        self.clock.tick(self.fps)
        time_passed = pygame.time.get_ticks() - start_time

      r_x = random.randint(300, 900)
      r_y = random.randint(380, 440)
      [car.reset(r_x, r_y) for car in self.steerable_cars]
      n_games += 1
    pygame.quit()
