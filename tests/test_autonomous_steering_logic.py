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

  def test_create_generation(self):
    result = self.logic.create_generation(5, 6)
    self.assertEqual(5, len(result))
    self.assertEqual(6, len(result[0]))

  def test_mutate_genome_with_high_probability(self):
    binary_genome = [0,0,0,1,1,0,1,0,0,1,0,0]
    self.logic.mutate_genome(binary_genome, probability=1.0)

    self.assertEqual([1,1,1,0,0,1,0,1,1,0,1,1], binary_genome)

if __name__ == '__main__':
  unittest.main()