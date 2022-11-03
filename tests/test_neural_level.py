import unittest
from neural_level import NeuralLevel

class TestNeuralLevel(unittest.TestCase):

  def test_number_of_weights(self):
    level = NeuralLevel(4, 5)
    self.assertEqual(25, level.number_of_weights())

if __name__ == '__main__':
  unittest.main()
