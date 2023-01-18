from base_program import BaseProgram
from genetic.genetic_program import GeneticProgram
from neat_dir.neat_program import NeatProgram
from deep_learning.game import Game
from deep_learning.game_env import GameEnv
from deep_learning.park_learning import ParkLearning

if __name__ == '__main__':
  # program = GeneticProgram()
  # program = Game()
  program = ParkLearning()
  program.ppo_learning()
  # program.dqn_learning()
  # program.a2c_learning()
  # program.random_check()
