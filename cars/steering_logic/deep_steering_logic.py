from deep_learning.neural_model import LinearQNet
from cars.steering_logic.steering_interface import SteeringInterface
import torch
import random
import math

EPS_START = 0.2
EPS_END = 0.05
EPS_DECAY = 500

class DeepSteeringLogic(SteeringInterface):

  def __init__(self):
    # Traning variables
    self.create_neural_network()
    self.set_games_and_steps(0, 0)
    self.last_action = None
    self.random_action_count = 0

  def create_neural_network(self):
    # Possible actions - Up, Down, UpLeft, UpRight, DownLeft, DownRight
    self.neural_network = LinearQNet(10, 6)

  def set_games_and_steps(self, n_games, total_steps):
    self.n_games = n_games
    self.total_steps = total_steps

  def get_steering_action(self, sensors_input):
    if self.random_action_count > 0:
      if self.random_action_count == 30:
        self.random_action_count = 0
      else:
        self.random_action_count += 1
        return self.last_action

    final_move = [0,0,0,0,0,0]
    sample = random.random()
    ex = math.exp(-1. * self.n_games / EPS_DECAY)
    eps_threshold = EPS_END + (EPS_START - EPS_END) * ex
    # print(eps_threshold)
    if sample > eps_threshold:
      # print('Not random')
      state0 = torch.tensor(sensors_input, dtype=torch.float)
      prediction = self.neural_network(state0)
      move = torch.argmax(prediction).item()
      final_move[move] = 1
    else:
      self.random_action_count = 1
      move = random.randint(0, 5)
      # print(f'Random move {move}')

      final_move[move] = 1

    self.last_action = final_move
    return final_move

  def get_steering_action2(self, sensors_input):
    # random moves: tradeoff exploration / exploitation
    epsilon = 80 - self.n_games
    final_move = [0,0,0,0,0,0]
    if random.randint(0, 200) < epsilon:
      move = random.randint(0, 5)
      # print(f'Random move {move}')

      final_move[move] = 1
    else:
      # print('Not random')
      state0 = torch.tensor(sensors_input, dtype=torch.float)
      prediction = self.neural_network(state0)
      move = torch.argmax(prediction).item()
      final_move[move] = 1

    self.last_action = final_move
    return final_move

  def get_steering_dict(self, sensors_input):
    final_move = self.get_steering_action(sensors_input)
    return self.map_steering(final_move)

  def map_steering(self, outputs):
    up = outputs[0]
    down = outputs[1]
    upleft = outputs[2]
    upright = outputs[3]
    downleft = outputs[4]
    downright = outputs[5]

    steering_dict = {
      'up': False,
      'down': False,
      'brake': False,
      'right': False,
      'left': False
    }

    if up == 1:
      steering_dict['up'] = True
    if down == 1:
      steering_dict['down'] = True

    if upleft == 1:
      steering_dict['up'] = True
      steering_dict['left'] = True
    if upright == 1:
      steering_dict['up'] = True
      steering_dict['right'] = True

    if downleft == 1:
      steering_dict['down'] = True
      steering_dict['left'] = True
    if downright == 1:
      steering_dict['down'] = True
      steering_dict['right'] = True
    return steering_dict

