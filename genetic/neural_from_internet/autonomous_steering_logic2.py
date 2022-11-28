from neural_network import NeuralNetwork
from genetic.neural_from_internet.feed_forward_network import FeedForwardNetwork, linear, sigmoid, tanh, relu, leaky_relu, ActivationFunction, get_activation_by_name
import numpy as np
class AutonomousSteeringLogic2:

  def __init__(self):
    self.create_neural_network()

  def set_chromosome(self, weights):
    weights_index = 0
    for l in range(1, len(self.network.layer_nodes)):
      for ll in range(0, len(self.network.params['W' + str(l)])):
        for lll in range(0, len(self.network.params['W' + str(l)][ll])):
          self.network.params['W' + str(l)][ll][lll] = weights[weights_index]
          weights_index += 1
        self.network.params['b' + str(l)][ll] = weights[weights_index]
        weights_index += 1

  def create_neural_network(self):
    self.network_architecture = [10]                          # Inputs
    self.network_architecture.extend([5,5])  # Hidden layers
    self.network_architecture.append(4)

    self.network = FeedForwardNetwork(self.network_architecture,
                                      get_activation_by_name('relu'),
                                      get_activation_by_name('sigmoid'))


    self.neural_network = NeuralNetwork()
    # Hidden layer and Output Layer
    self.neural_network.add_level(10, 5)
    self.neural_network.add_level(5, 5)
    self.neural_network.add_level(5, 4)

  def set_neural_weights(self, weights):
    self.set_chromosome(weights)
    # self.network.params = chromosome
    # self.neural_network.set_weights(weights)

  def number_of_network_weights(self):
    return self.neural_network.number_of_weights()

  def convert_to_movment_signal(self, sigmoid_value, margin = 0.4):
    if sigmoid_value > (0.9):
      return 1
    else:
      return 0

  def get_steering_dict(self, sensors_input):
    ss = np.asarray(sensors_input)
    ss = ss.reshape(10,1)
    self.network.feed_forward(ss)
    out = self.network.out.flatten()
    ew = [self.convert_to_movment_signal(s) for s in out]
    # print('results ')
    # print(ew)
    up = ew[0]
    down = ew[1]
    left = ew[2]
    right = ew[3]

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

    if left == 1:
      steering_dict['left'] = True
    if right == 1:
      steering_dict['right'] = True
    return steering_dict

