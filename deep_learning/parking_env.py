import gym
from gym import spaces
import numpy as np
from deep_learning.reinforcement_program import ReinforcementProgram

class ParkingEnv(gym.Env):

  def __init__(self):
    super(ParkingEnv, self).__init__()
    self.game = ReinforcementProgram()
    self.action_space = spaces.Discrete(7)
    self.observation_space = spaces.Box(low=-1, high=25,
                      shape=(11,), dtype=np.float64)

  def step(self, action):
    return self.game.step(action)

  def reset(self):
    return self.game.reset()

  def can_close(self):
    return self.game.can_close()

  def close(self):
    self.game.close()
