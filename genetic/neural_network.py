from genetic.neural_level import NeuralLevel

class NeuralNetwork:

  def __init__(self):
    self.levels = []

  def set_weights(self, weights):
    self.current_weight_index = 0

    for level in self.levels:
      weights_for_level = self.slice_weights_for_level(weights, level)
      level.set_weights(weights_for_level)

  def compute_output(self, input_data):
    for level in self.levels:
      input_data = level.calculate_neuron_outputs(input_data)
    return input_data

  def slice_weights_for_level(self, weights, level):
    # Each nueron has connect with all input data and has additional Bias weight
    end_index = self.current_weight_index + level.number_of_weights()
    result = weights[self.current_weight_index:end_index]
    self.current_weight_index = end_index
    return result

  def add_level(self, input_number, neuron_number):
    # Check if output number of the last added level is the same with input number of the level to add
    if self.levels and (self.levels[-1].neuron_number != input_number):
      raise Exception("Levels in the network have incompatible input and output numbers")

    for level in self.levels:
      level.is_output = False

    self.levels.append(NeuralLevel(input_number, neuron_number, is_output=True))

  def number_of_weights(self):
    weights_number = 0
    for level in self.levels:
      weights_number += level.number_of_weights()
    return weights_number
