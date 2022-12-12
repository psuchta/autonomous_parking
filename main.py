from base_program import BaseProgram
from genetic.genetic_program import GeneticProgram
from neat_dir.neat_program import NeatProgram
from deep_learning.deep_program import DeepProgram

if __name__ == '__main__':
  # program = GeneticProgram()
  # program = NeatProgram()
  program = DeepProgram()
  program.run()
