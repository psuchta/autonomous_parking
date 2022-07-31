import unittest
import numpy as np
from genome import Genome
import random

class TestGenome(unittest.TestCase):
  def setUp(self):
    self.genome = Genome()

  def test_constants(self):
    self.assertEqual(176, Genome.PEER_STEER_GENES)
    self.assertEqual(352, Genome.GENOME_LENGTH)

  def test_genome_to_decimals_with_invalid_length(self):
    with self.assertRaisesRegex(Exception, "Length of passed genome is not correct"):
      self.genome.genome_to_decimals([0,1,0,1,0,1,0,1,1,1,0,1])

  def test_genome_to_decimals_returns_correct_result(self):
    binary = []
    binary.extend([0,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1]) # 24.3
    binary.extend([1,1,0,1,0,1,1,1,1,0,1,0,1,0,0,0]) # -122.5
    binary.extend([1,1,0,0,1,0,0,0,1,0,0,0,1,1,1,1]) # -9.12

    for i in range(len(binary),Genome.GENOME_LENGTH): 
      binary += str(random.randint(0, 1))

    self.assertEqual(len(binary), Genome.GENOME_LENGTH)
    result = self.genome.genome_to_decimals(binary)

    self.assertEqual(np.float16(24.3), result[0])
    self.assertEqual(np.float16(-122.5), result[1])
    self.assertEqual(np.float16(-9.12), result[2])

  def engine_wheels_signal(self, binary_genome):
    binary = []
    for idx in range(0, Genome.PEER_STEER_GENES):
      binary.extend([0,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1]) # 24.31

    for idx in range(Genome.PEER_STEER_GENES, Genome.GENOME_LENGTH):
      binary.extend([1,1,0,1,0,1,1,1,1,0,1,0,1,0,0,0]) # -122.5

    engine_signal, wheels_signal = self.genome.genome_to_decimals(binary)
    self.assertEqual(np.float16(24.31), engine_signal[0])
    self.assertEqual(np.float16(-122.5), wheels_signal[0])

if __name__ == '__main__':
  unittest.main()