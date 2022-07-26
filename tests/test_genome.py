import unittest
import numpy as np
from genome import Genome
import random

class TestGenome(unittest.TestCase):
  def setUp(self):
    self.genome = Genome()

  def test_constants(self):
    self.assertEqual(176, Genome.STEER_FORMULA_GENES_NUM)
    self.assertEqual(352, Genome.GENOME_LENGTH)

  def test_binary_to_decimals_with_invalid_length(self):
    with self.assertRaisesRegex(Exception, "Length of passed genome is not correct"):
      self.genome.binary_to_decimals('010101011101')

  def test_binary_to_decimals_returns_correct_result(self):
    binary = ''
    binary += '0100111000010100' # 24.32
    binary += '1101011110101000' # -122.5
    binary += '1100100010001111' # -9.12

    for i in range(len(binary),Genome.GENOME_LENGTH): 
      binary += str(random.randint(0, 1))

    self.assertEqual(len(binary), Genome.GENOME_LENGTH)
    result = self.genome.binary_to_decimals(binary)

    self.assertEqual(np.float16(24.31), result[0])
    self.assertEqual(np.float16(-122.5), result[1])
    self.assertEqual(np.float16(-9.12), result[2])


if __name__ == '__main__':
  unittest.main()