from neural_network import NeuralNetwork

class AutonomousSteeringLogic:

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

  def map_steering(self, outputs):
    up = outputs[0]
    down = outputs[1]
    left = outputs[2]
    right = outputs[3]

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


  def get_steering_dict(self, sensors_input):
    outputs = self.neural_network.compute_output(sensors_input)
    return self.map_steering(outputs)

