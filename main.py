from base_program import BaseProgram
from genetic.genetic_program import GeneticProgram
from neat_dir.neat_program import NeatProgram

if __name__ == '__main__':
  # program = GeneticProgram()
  program = NeatProgram()
  program.run()
