from deep_learning.neural_model import LinearQNet
from cars.steering_logic.steering_interface import SteeringInterface
import torch
import random

class DeepSteeringLogic(SteeringInterface):

  def __init__(self):
    # Traning variables
    self.learning_rate = 0.001
    self.gamma = 0.7 # discount rate
    self.create_neural_network()
    self.set_n_games(0)
    self.last_action = None

  def create_neural_network(self):
    # Possible actions - Up, Down, UpLeft, UpRight, DownLeft, DownRight
    self.neural_network = LinearQNet(10, 6)

  def set_n_games(self, n_games):
    self.n_games = n_games

  def get_steering_action(self, sensors_input):
    # random moves: tradeoff exploration / exploitation
    epsilon = 80 - self.n_games
    final_move = [0,0,0,0,0,0]
    # print(f'N Game = ${self.n_games}')
    # print('epsilon')
    # print(epsilon)
    if random.randint(0, 200) < epsilon:
      move = random.randint(0, 5)
      # print(f'Random move {move}')

      final_move[move] = 1
    else:
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

