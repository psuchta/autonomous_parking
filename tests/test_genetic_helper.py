import unittest
from unittest.mock import patch
from genetic_helper import GeneticHelper
from genome_helper import GenomeHelper

class TestGeneticHelper(unittest.TestCase):
  def setUp(self):
    self.genetic_helper = GeneticHelper()

  def test_crossover(self):
    with patch('random.randint', return_value=3) as mock_random:
      result = self.genetic_helper.crossover([0, 1, 0, 1, 1, 0, 1],[1, 1, 0, 1, 0, 1, 0])
      self.assertEqual(([0, 1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0, 1] ), result)

  def test_crossover_ieee_754(self):
    with patch('random.randint', return_value=4) as mock_random:
      result = self.genetic_helper.crossover_ieee_754([1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1],[0,1,1,0,1,0,0,1,1,0,1,0,1,0,0,0])
      self.assertEqual(([1,0,1,1,1,0,0,1,1,0,1,0,1,0,0,0], [0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1] ), result)

  def test_crossover_with_incompatibile_arrays(self):
    with self.assertRaisesRegex(Exception, "Lengths of passed arrays are not the same"):
      self.genetic_helper.crossover([0, 1, 0,], [1, 0])

  def test_mutate_genome_with_high_probability(self):
    binary_genome = [0,0,0,1,1,0,1,0,0,1,0,0]
    self.genetic_helper.mutate_genome(binary_genome, probability=1.0)

    self.assertEqual([1,1,1,0,0,1,0,1,1,0,1,1], binary_genome)

  def test_mutate_ieee_754_genome_with_high_probability(self):
    binary_genome = [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1, 1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1]
    self.genetic_helper.mutate_ieee_754_genome(binary_genome, probability=1.0)

    self.assertEqual([0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,  0,0,0,0,0,0,0,1,1,0,1,1,1,1,0,0], binary_genome)

  def test_create_random_generation(self):
    result = self.genetic_helper.create_random_generation(5, 2)
    self.assertEqual(5, len(result))
    self.assertEqual(2 * GenomeHelper.GENES_PER_NUMBER , len(result[0]))


if __name__ == '__main__':
  unittest.main()
