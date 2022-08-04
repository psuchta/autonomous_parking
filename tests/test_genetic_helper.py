import unittest
from unittest.mock import patch
from genetic_helper import GeneticHelper

class TestGeneticHelper(unittest.TestCase):
  def setUp(self):
    self.genetic_helper = GeneticHelper()

  def test_crossover(self):
    with patch('random.randint', return_value=3) as mock_random:
      result = self.genetic_helper.crossover([0, 1, 0, 1, 1, 0, 1],[1, 1, 0, 1, 0, 1, 0])
      self.assertEqual(([0, 1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0, 1] ), result)

  def test_crossover_with_incompatibile_arrays(self):
    with self.assertRaisesRegex(Exception, "Lengths of passed arrays are not the same"):
      self.genetic_helper.crossover([0, 1, 0,], [1, 0])

  def test_mutate_genome_with_high_probability(self):
    binary_genome = [0,0,0,1,1,0,1,0,0,1,0,0]
    self.genetic_helper.mutate_genome(binary_genome, probability=1.0)

    self.assertEqual([1,1,1,0,0,1,0,1,1,0,1,1], binary_genome)

  def test_create_generation(self):
    result = self.genetic_helper.create_generation(5, 6)
    self.assertEqual(5, len(result))
    self.assertEqual(6, len(result[0]))


if __name__ == '__main__':
  unittest.main()