from deep_learning.neural_model import LinearQNet, QTrainer
from cars.steering_logic.steering_interface import SteeringInterface
import torch

class DeepSteeringLogic(SteeringInterface):

  def __init__(self):
    # Traning variables
    self.learning_rate = 0.001
    self.gamma = 0.9 # discount rate
    self.create_neural_network()

  def create_neural_network(self):
    # Possible actions - Up, Down, UpLeft, UpRight, DownLeft, DownRight
    self.neural_network = LinearQNet(10, 6)
    self.trainer = QTrainer(self.neural_network, lr=self.learning_rate, gamma=self.gamma)

  def get_steering_dict(self, sensors_input):
    final_move = [0,0,0,0,0,0]
    state0 = torch.tensor(sensors_input, dtype=torch.float)
    prediction = self.neural_network(state0)
    move = torch.argmax(prediction).item()
    final_move[move] = 1
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

