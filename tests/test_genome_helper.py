import unittest
import numpy as np
from genome_helper import GenomeHelper
import random

class TestGenome(unittest.TestCase):
  def setUp(self):
    self.genome_helper = GenomeHelper()

  def test_constants(self):
    self.assertEqual(16, GenomeHelper.GENES_PER_NUMBER)

  def test_genome_to_decimals_with_invalid_length(self):
    with self.assertRaisesRegex(Exception, "Length of passed genome is not correct"):
      self.genome_helper.genome_to_decimals([0,1,0,1,0,1,0,1,1,1,0,1])

  def test_genome_to_decimals_returns_correct_result(self):
    binary = []
    binary.extend([0,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1]) # 24.3
    binary.extend([1,1,0,1,0,1,1,1,1,0,1,0,1,0,0,0]) # -122.5
    binary.extend([1,1,0,0,1,0,0,0,1,0,0,0,1,1,1,1]) # -9.12

    result = self.genome_helper.genome_to_decimals(binary)

    self.assertEqual(np.float16(24.3), result[0])
    self.assertEqual(np.float16(-122.5), result[1])
    self.assertEqual(np.float16(-9.12), result[2])

  def test_init_randomly(self):
    numbers_in_genome = 20

    binary_genome = self.genome_helper.init_randomly(numbers_in_genome)
    genome_length = numbers_in_genome * GenomeHelper.GENES_PER_NUMBER

    self.assertEqual(genome_length, len(binary_genome))
    self.assertTrue(binary_genome[0] == 0 or 1 )
    self.assertTrue(binary_genome[1] == 0 or 1 )

  def test_init_number_randomly(self):
    binary_genome = self.genome_helper.init_number_randomly(5, 6)
    # 1 sign bit, 5 exponent bits, 6 significand bits
    self.assertEqual(12, len(binary_genome))
    self.assertTrue(binary_genome[0] == 0 or 1 )
    self.assertTrue(binary_genome[1] == 0 or 1 )

  def test_check_if_any_number_forbidden_with_error(self):
    with self.assertRaisesRegex(Exception, "Binary number has wrong length"):
      self.genome_helper.check_if_any_number_forbidden([0,1,1,0,0,0,0,1,0,0,1,1])

  def test_check_if_any_number_forbidden(self):
    is_forbidden = self.genome_helper.check_if_any_number_forbidden([1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
    self.assertEqual(True, is_forbidden)    

    is_forbidden = self.genome_helper.check_if_any_number_forbidden([0,1,1,1,1,1,0,0,0,0,1,0,0,1,0,1,  0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,1])
    self.assertEqual(True, is_forbidden)

    is_forbidden = self.genome_helper.check_if_any_number_forbidden([0,1,1,0,1,1,0,0,0,0,0,1,0,0,1,1, 1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1])
    self.assertEqual(False, is_forbidden)

  def test_check_if_number_forbidden(self):
    with self.assertRaisesRegex(Exception, "Binary number has wrong length"):
      self.genome_helper.check_if_any_number_forbidden([0,1,1,0,0,0,1,1])

    is_forbidden = self.genome_helper.check_if_number_forbidden([1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
    self.assertEqual(True, is_forbidden)    

    is_forbidden = self.genome_helper.check_if_number_forbidden([1,1,1,1,1,1,0,0,0,1,0,0,1,0,1,1])
    self.assertEqual(True, is_forbidden)

    is_forbidden = self.genome_helper.check_if_number_forbidden([1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1])
    self.assertEqual(False, is_forbidden)

    is_forbidden = self.genome_helper.check_if_number_forbidden([0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1])
    self.assertEqual(False, is_forbidden)

    is_forbidden = self.genome_helper.check_if_number_forbidden([0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1])
    self.assertEqual(False, is_forbidden)



if __name__ == '__main__':
  unittest.main()
