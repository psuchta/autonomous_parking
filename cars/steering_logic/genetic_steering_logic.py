from genetic.neural_network import NeuralNetwork
from cars.steering_logic.steering_interface import SteeringInterface

class GeneticSteeringLogic(SteeringInterface):

  def __init__(self):
    self.create_neural_network()

  def create_neural_network(self):
    self.neural_network = NeuralNetwork()
    # Hidden layer and Output Layer
    self.neural_network.add_level(10, 10)
    self.neural_network.add_level(10, 10)
    self.neural_network.add_level(10, 4)

  def set_neural_weights(self, weights):
    self.neural_network.set_weights(weights)

  def number_of_network_weights(self):
    return self.neural_network.number_of_weights()

  def get_steering_dict(self, sensors_input):
    outputs = self.neural_network.compute_output(sensors_input)
    move_outputs = [ self.convert_to_movment_signal(o) for o in outputs]
    return self.map_steering(move_outputs)

