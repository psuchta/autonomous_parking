import unittest
import numpy as np
from binary_converter import BinaryConverter

class TestBinaryConverter(unittest.TestCase):
  def setUp(self):
    self.logic = BinaryConverter()

#####IEEE754 conversion######
  def test_float_to_bin(self):
    result = self.logic.float_to_bin(17.5)
    self.assertEqual('0100110001100000', result)

    result = self.logic.float_to_bin(0.059)
    self.assertEqual('0010101110001101', result)

    result = self.logic.float_to_bin(-21.085)
    self.assertEqual('1100110101000101', result)

  def test_bin_to_float(self):
    result = self.logic.bin_to_float('0100110001100000')
    self.assertEqual(17.5, result)

    result = self.logic.bin_to_float('0010101110001101')
    self.assertEqual(np.float16(0.059), result)

    result = self.logic.bin_to_float('1100110101000101')
    self.assertEqual(np.float16(-21.085), result)

if __name__ == '__main__':
  unittest.main()