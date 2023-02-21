from genetic.neural_layer import NeuralLayer

class NeuralNetwork:

  def __init__(self):
    self.layers = []

  def set_weights(self, weights):
    self.current_weight_index = 0

    for layer in self.layers:
      weights_for_layer = self.slice_weights_for_layer(weights, layer)
      layer.set_weights(weights_for_layer)

  def compute_output(self, input_data):
    for layer in self.layers:
      input_data = layer.calculate_neuron_outputs(input_data)
    return input_data

  def slice_weights_for_layer(self, weights, layer):
    # Each nueron has connect with all input data and has additional Bias weight
    end_index = self.current_weight_index + layer.number_of_weights()
    result = weights[self.current_weight_index:end_index]
    self.current_weight_index = end_index
    return result

  def add_layer(self, input_number, neuron_number):
    # Check if output number of the last added layer is the same with input number of the layer to add
    if self.layers and (self.layers[-1].neuron_number != input_number):
      raise Exception("layers in the network have incompatible input and output numbers")

    for layer in self.layers:
      layer.is_output = False

    self.layers.append(NeuralLayer(input_number, neuron_number, is_output=True))

  def number_of_weights(self):
    weights_number = 0
    for layer in self.layers:
      weights_number += layer.number_of_weights()
    return weights_number
