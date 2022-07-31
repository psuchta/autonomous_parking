import unittest
import numpy as np
from binary_converter import BinaryConverter

class TestBinaryConverter(unittest.TestCase):
  def setUp(self):
    self.logic = BinaryConverter()

#####IEEE754 conversion######
  def test_float_to_bin(self):
    result = self.logic.float_to_bin(17.5)
    self.assertEqual([0,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0], result)

    result = self.logic.float_to_bin(0.059)
    self.assertEqual([0,0,1,0,1,0,1,1,1,0,0,0,1,1,0,1], result)

    result = self.logic.float_to_bin(-21.085)
    self.assertEqual([1,1,0,0,1,1,0,1,0,1,0,0,0,1,0,1], result)

  def test_bin_to_float(self):
    result = self.logic.bin_to_float([0,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0])
    self.assertEqual(17.5, result)

    result = self.logic.bin_to_float([0,0,1,0,1,0,1,1,1,0,0,0,1,1,0,1])
    self.assertEqual(np.float16(0.059), result)

    result = self.logic.bin_to_float([1,1,0,0,1,1,0,1,0,1,0,0,0,1,0,1])
    self.assertEqual(np.float16(-21.085), result)

  def test_string_to_int_array(self):
    result = self.logic.string_to_int_array('00111011001')
    self.assertEqual([0,0,1,1,1,0,1,1,0,0,1], result)

if __name__ == '__main__':
  unittest.main()