from base_program import BaseProgram
from genetic.genetic_program import GeneticProgram
from neat_dir.neat_program import NeatProgram
from deep_learning.parking_env import ParkingEnv
from deep_learning.park_learning import ParkLearning

if __name__ == '__main__':
  program = GeneticProgram()
  # program = NeatProgram()
  program.run()
  # NEAT Loading form file 
  # program.run_from_file()

  # program = ParkLearning()
  # program.ppo_learning()
  # program.ppo_from_file()
  # program.random_check()
  # program.dqn_learning()
  # program.a2c_learning()
