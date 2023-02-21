import numpy as np
import math

class NeuralLayer:
  def __init__(self, input_number, neuron_number, is_output=False):
    self.input_number = input_number
    self.neuron_number = neuron_number
    self.neuron_weights = []
    self.neuron_biases = []
    self.is_output = is_output

  def set_weights(self, weights):
    if len(weights) != self.number_of_weights():
      raise Exception("Length of weights array is incorrect")

    weights_for_neuron = self.input_number
    np_weights = np.array(weights)
    
    # Split weights for each neuron
    weights_per_neurons = np.array_split(np_weights, self.neuron_number)

    weights_matrix = []
    biases = []
    for i in range(0, self.neuron_number):
      weights_matrix.append(weights_per_neurons[i][0:weights_for_neuron])
      biases.append([weights_per_neurons[i][-1]])
     
    self.neuron_weights = np.array(weights_matrix)
    self.neuron_biases = np.array(biases)

  def calculate_neuron_outputs(self, input_data):
    input_data_column = np.array([input_data]).transpose()

    multi = self.neuron_weights.dot(input_data_column)
    res = multi + self.neuron_biases
    res_flatten = res.flatten()
    if self.is_output:
      return [ self.sigmoid(r) for r in res_flatten]
    else:
      return [self.relu(r) for r in res_flatten]
    
  def sigmoid(self, x):
    return 1.0 / (1.0 + np.exp(-x))

  def relu(self, x):
    return np.maximum(0, x)

  def tanh(self, x):
    return math.tanh(x)

  def convert_to_movment_signal(self, sigmoid_value, margin = 0.4):
    if sigmoid_value > (0.9):
      return 1
    else:
      return 0

  def number_of_weights(self):
    return self.input_number * self.neuron_number + self.neuron_number
