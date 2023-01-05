from cars.steering_logic.steering_interface import SteeringInterface
import torch
import random
import math

EPS_START = 0.7
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
    self.neural_network = LinearQNet(11, 6)

  def get_steering_action(self, sensors_input):

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

