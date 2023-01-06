import gym
from gym import spaces
import numpy as np
# import cv2
import random
import time
from collections import deque
from deep_learning.game import Game

class GameEnv(gym.Env):

  def __init__(self):
    super(GameEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    self.game = Game()
    self.action_space = spaces.Discrete(6)
    # Example for using image as input (channel-first; channel-last also works):
    self.observation_space = spaces.Box(low=-25, high=700,
                      shape=(11,), dtype=np.float64)

  def step(self, action):
    return self.game.step()

  def reset(self):
    return self.game.reset()

  def can_close(self):
    return self.game.can_close()

  def close(self):
    self.game.close()