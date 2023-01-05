from base_program import BaseProgram
from deep_learning.neural_model import QTrainer
from cars.deep_controlled_car import DeepControlledCar
from collections import deque
import pygame
import random
import numpy as np
from genetic.genetic_helper import GeneticHelper
from torch.utils.tensorboard import SummaryWriter
# from memory import ReplayMemory

MAX_MEMORY = 1000000
BATCH_SIZE = 64
LR = 0.00025
GAMMA = 0.9


class DeepProgram(BaseProgram):
  def __init__(self):
    self.writer = SummaryWriter('runs/fashion_mnist_experiment_1')
    self.genetic_helper = GeneticHelper()
    self.memory = deque(maxlen=MAX_MEMORY) # popleft()
    BaseProgram.__init__(self)
    self.autonomous_car = self.steerable_cars[0]
    self.car_steering_model = self.autonomous_car.autonomous_steering_logic.neural_network
    self.car_steering_logic = self.autonomous_car.autonomous_steering_logic
    self.trainer = QTrainer(self.car_steering_model, lr=LR, gamma=GAMMA)

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    car = DeepControlledCar(700, 430, self.screen, self)
    self.add_car(car)
    car.set_parking_spot(self.parking_slot)

  def remember(self, state_old, last_action, reward, state_new, is_done):
    self.memory.append((state_old, last_action, reward, state_new, is_done)) # popleft if MAX_MEMORY is reached

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
    self.car_steering_logic.set_games_and_steps(n_games, self.total_steps)
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

  def train_short_memory(self, state_old, last_action, reward, state_new, is_done):
    return self.trainer.train_step(state_old, last_action, reward, state_new, is_done)

  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
        mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
    else:
        mini_sample = self.memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    return self.trainer.train_step(states, actions, rewards, next_states, dones)

  def train(self, n_games, dt):
    state_old = self.get_state()
    reward, is_done = self.play_step(n_games, dt)
    last_action = self.car_steering_logic.last_action
    state_new = self.get_state()

    # train short memory
    # loss = self.train_short_memory(state_old, last_action, reward, state_new, is_done)
    loss = None
    self.remember(state_old, last_action, reward, state_new, is_done)
    return (reward, loss)


  def run(self):
    n_games = 0
    self.total_steps = 0
    scores = []
    episode_index = 0
    while not self.exit:
      long_running_loss = 0
      start_time = pygame.time.get_ticks()
      time_passed = 0
      score = 0 
      self.previous_fitness = 0
      short_running_loss = 0
      episode_index = 0
      while not self.exit and any(car.alive for car in self.steerable_cars) and time_passed <= 10000:
        dt = self.clock.get_time() / 1000
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.exit = True      
        reward, short_loss = self.train(n_games, dt)
        # short_running_loss += short_loss
        score += reward
        # self.genetic_helper.fitness(self.autonomous_car, self.parking_slot)
        pygame.display.flip()
        self.clock.tick(self.fps)
        time_passed = pygame.time.get_ticks() - start_time
        episode_index += 1
        if episode_index % 100 == 0:
          # print('Loss', short_running_loss/100, ' ', self.total_steps)
          self.writer.add_scalar('Loss', short_running_loss/100, self.total_steps)

      # train long memory, plot result
      long_running_loss += self.train_long_memory()
      self.writer.add_scalar('Long loss', long_running_loss, n_games)
      
      scores.append(score)
      avg_score =  np.mean(scores[-100:])
      print('game ', n_games, 'score %.2f' %score, 'avg_score %.2f' % avg_score)

      r_x = random.randint(300, 900)
      r_y = random.randint(380, 440)
      [car.reset(r_x, r_y) for car in self.steerable_cars]
      n_games += 1

      # save neural model every 25 done games
      if n_games % 25 == 0:
        self.car_steering_model.save()
    self.writer.flush()
    self.writer.close()
    pygame.quit()
