import unittest
from neural_layer import NeuralLayer

class TestNeuralLayer(unittest.TestCase):

  def test_number_of_weights(self):
    layer = NeuralLayer(4, 5)
    self.assertEqual(25, layer.number_of_weights())

if __name__ == '__main__':
  unittest.main()
