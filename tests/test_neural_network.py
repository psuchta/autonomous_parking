import unittest
import numpy as np
from neural_network import NeuralNetwork

class TestNeuralNetwork(unittest.TestCase):
  def setUp(self):
    self.neural_network = NeuralNetwork()
    self.neural_network.add_level(3, 2)
    self.neural_network.add_level(2, 1)

  def test_set_weights(self):
    # FIRST NEURAL LEVEL
    # First neuron weights
    weights = [1.5, 2.5, 1.2, 2]
    # Second neuron weights
    weights.extend([2.3, 3.1, 2.8, 1])
    # SECOND NEURAL LEVEL weights
    weights.extend([3.1, 2.9, 4])

    self.neural_network.set_weights(weights)
    # Check First Neural Level 
    np.testing.assert_array_equal([[1.5, 2.5, 1.2], [2.3, 3.1, 2.8]], self.neural_network.levels[0].neuron_weights)
    np.testing.assert_array_equal([[2], [1]], self.neural_network.levels[0].neuron_biases)
    self.assertEqual(False, self.neural_network.levels[0].is_output)
    # Check Second Neural Level 
    np.testing.assert_array_equal([[3.1, 2.9]], self.neural_network.levels[1].neuron_weights)
    np.testing.assert_array_equal([[4]], self.neural_network.levels[1].neuron_biases)
    self.assertEqual(True, self.neural_network.levels[1].is_output)

  def test_calculate_neuron_outputs(self):
    # FIRST NEURAL LEVEL
    # First neuron weights
    weights = [1.5, -2.5, 1.2, -2]
    # Second neuron weights
    weights.extend([2.3, 3.1, -2.8, -1])
    # SECOND NEURAL LEVEL weights
    weights.extend([3.1, 2.9, -2])
    self.neural_network.set_weights(weights)

    # Check First Neural Level 
    result = self.neural_network.levels[0].calculate_neuron_outputs([3, 4, 7])
    self.assertEqual([0.710949502625004, 0.21416501695744186], result)
    # Check Second Neural Level 
    result2 = self.neural_network.levels[1].calculate_neuron_outputs([0.710949502625004, 0.21416501695744186])
    self.assertEqual([0], result2)
    # Overall Neural Network Output
    self.assertEqual([0], self.neural_network.compute_output([3, 4, 7]))

if __name__ == '__main__':
  unittest.main()
