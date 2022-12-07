import neat
from cars.steering_logic.steering_interface import SteeringInterface

class NeatSteeringLogic(SteeringInterface):

  def __init__(self):
    self.create_neural_network()

  def create_neural_network(self):
    self.neural_network = None

  def set_neural_weights(self, weights, config):
    self.neural_network = neat.nn.FeedForwardNetwork.create(weights, config)

  def get_steering_dict(self, sensors_input):
    outputs = self.neural_network.activate(sensors_input)
    move_outputs = [ self.convert_to_movment_signal(o) for o in outputs]
    return self.map_steering(move_outputs)

