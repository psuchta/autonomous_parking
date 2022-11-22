import unittest
from unittest.mock import patch
from genetic_helper import GeneticHelper
from genome_helper import GenomeHelper
from unittest.mock import Mock

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
    binary_genome = [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1, 1,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1]
    self.genetic_helper.mutate_ieee_754_genome(binary_genome, probability=1.0)

    self.assertEqual([0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,  0,0,1,0,0,0,0,1,1,0,1,1,1,1,0,0], binary_genome)

  def test_mutate_ieee_754_genome_with_low_probability(self):
    binary_genome = [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1, 1,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1]
    self.genetic_helper.mutate_ieee_754_genome(binary_genome, probability=0.00001)
    self.assertEqual([1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1, 1,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1], binary_genome)

  def test_create_random_generation(self):
    result = self.genetic_helper.create_random_generation(5, numbers_per_genome=2)
    self.assertEqual(5, len(result))
    self.assertEqual(2 * GenomeHelper.GENES_PER_NUMBER , len(result[0]))

  def test_tournament_selection(self):
    car_population = [Mock(fitness=3), Mock(fitness=2), Mock(fitness=1)]
    # car_population, tournament_size
    selected_population = self.genetic_helper.tournament_selection(car_population, 3)
    fitness_results = [car.fitness for car in selected_population]

    self.assertEqual([3, 3, 3], fitness_results)

  def test_genetic_program_flow(self):
    self.genome_helper = GenomeHelper()

    car_population = [Mock(fitness=3, genome=self.genome_helper.init_number_randomly()), Mock(fitness=2, genome=self.genome_helper.init_number_randomly())]
    selected_population = self.genetic_helper.tournament_selection(car_population, 2)

    for i in range(0, len(selected_population)-1, 2):
      child1, child2 = self.genetic_helper.crossover_ieee_754(selected_population[i].genome, selected_population[i+1].genome)
      self.genetic_helper.mutate_ieee_754_genome(child1, 0.5)
      self.genetic_helper.mutate_ieee_754_genome(child2, 0.5)

      selected_population[i].genome = child1
      selected_population[i+1].genome = child2



if __name__ == '__main__':
  unittest.main()
