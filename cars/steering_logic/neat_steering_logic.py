class NeatSteeringLogic:

  def __init__(self):
    self.create_neural_network()

  def create_neural_network(self):
    self.neural_network = None

  def set_neural_weights(self, weights):
    self.neural_network.set_weights(weights)

  def get_steering_dict(self, sensors_input):
    outputs = self.neural_network.compute_output(sensors_input)
    return self.map_steering(outputs)

