from base_program import BaseProgram
from deep_learning.neural_model import QTrainer
from cars.deep_controlled_car import DeepControlledCar
from collections import deque
import pygame
import random
import numpy as np
from genetic.genetic_helper import GeneticHelper
# from memory import ReplayMemory

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DeepProgram(BaseProgram):
  def __init__(self):
    self.genetic_helper = GeneticHelper()
    self.memory = deque(maxlen=MAX_MEMORY) # popleft()
    self.gamma = 0.9
    BaseProgram.__init__(self)
    self.autonomous_car = self.steerable_cars[0]
    self.car_steering_model = self.autonomous_car.autonomous_steering_logic.neural_network
    self.car_steering_logic = self.autonomous_car.autonomous_steering_logic
    self.trainer = QTrainer(self.car_steering_model, lr=LR, gamma=self.gamma)

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    car = DeepControlledCar(700, 430, self.screen, self)
    self.add_car(car)

  def remember(self, state_old, last_action, reward, state_new, is_done):
    self.memory.append((state_old, last_action, reward, state_new, is_done)) # popleft if MAX_MEMORY is reached

  def get_state(self):
    state = self.autonomous_car.get_sensors_data()
    return np.array(state, dtype=float)

  def play_step(self, n_games, delta_time):
    self.draw_objects(delta_time)
    self.draw_generation_num(n_games)
    current_fitness = self.genetic_helper.fitness(self.autonomous_car, self.parking_slot)
    delta_fintness = current_fitness - self.last_fitness
    reward = 0
    if delta_fintness < 0:
      reward = -10
    elif delta_fintness > 0:
      reward = 10
    # print(reward)
    self.last_fitness = current_fitness
    # Did car hit something
    is_done = not self.autonomous_car.alive
    return reward, is_done

  def draw_generation_num(self, gen_num):
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Generation:' + str(gen_num), True, (255, 255, 255))
    self.screen.blit(text, (20,10))

  def train_short_memory(self, state_old, last_action, reward, state_new, is_done):
    self.trainer.train_step(state_old, last_action, reward, state_new, is_done)

  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
        mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
    else:
        mini_sample = self.memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    self.trainer.train_step(states, actions, rewards, next_states, dones)

  def train(self, n_games, dt):
    state_old = self.get_state()
    reward, is_done = self.play_step(n_games, dt)
    last_action = self.car_steering_logic.last_action
    state_new = self.get_state()

    # train short memory
    self.train_short_memory(state_old, last_action, reward, state_new, is_done)
    self.remember(state_old, last_action, reward, state_new, is_done)


  def run(self):
    n_games = 0
    while not self.exit:
      self.car_steering_logic.set_n_games(n_games)
      start_time = pygame.time.get_ticks()
      time_passed = 0
      self.last_fitness = 0
      while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 100000:
        dt = self.clock.get_time() / 1000
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.exit = True      
        self.train(n_games, dt)
        # self.genetic_helper.fitness(self.autonomous_car, self.parking_slot)
        pygame.display.flip()
        self.clock.tick(self.fps)
        time_passed = pygame.time.get_ticks() - start_time

      # train long memory, plot result
      self.train_long_memory()
      print(len(self.memory))
      
      [car.reset(700, 430) for car in self.steerable_cars]
      n_games += 1
    pygame.quit()
