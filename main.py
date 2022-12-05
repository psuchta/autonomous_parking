from base_program import BaseProgram
from genetic_program import GeneticProgram
from neat.neat_program import NeatProgram

if __name__ == '__main__':
  program = GeneticProgram()
  # program = NeatProgram()
  program.run()
