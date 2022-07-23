import unittest
import numpy as np
from autonomous_steering_logic import AutonomousSteeringLogic

class TestAutonomousSteeringLogic(unittest.TestCase):
  def setUp(self):
    self.logic = AutonomousSteeringLogic()

######linear_polynomial######
  def test_linear_polynomial_wrong_array_size(self):
    with self.assertRaises(Exception):
      self.logic.linear_polynomial([1,2,3],[1])

  def test_linear_polynomial_return_correct_result(self):
    result = self.logic.linear_polynomial([1,2,3,4,5],[2,2,2,2])
    self.assertEqual(25,result)

######sigmoid######
  def test_sigmoid(self):
    result = self.logic.sigmoid(25)
    self.assertEqual(0.999999999986112, result)

    result = self.logic.sigmoid(-0.5)
    self.assertEqual(0.3775406687981454, result)

    result = self.logic.sigmoid(-200)
    self.assertEqual(1.383896526736752e-87, result)


#####convert_to_movment_signal######
  def test_linear_polynomial_return_correct_result(self):
    result = self.logic.convert_to_movment_signal(0.9999)
    self.assertEqual(1,result)

    result = self.logic.convert_to_movment_signal(0.60001)
    self.assertEqual(0,result)

    result = self.logic.convert_to_movment_signal(0.099999)
    self.assertEqual(-1,result)

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