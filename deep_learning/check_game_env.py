from stable_baselines3.common.env_checker import check_env
from deep_learning.game_env import GameEnv


class CheckGameEnv():
  def __init__(self):
    self.env = GameEnv()

  def simple_check(self):
    check_env(self.env)

  def double_check(self):
    done = False

    obs = self.env.reset()
    while not self.env.can_close():
      # print(self.env.can_close())
      obs, reward, done, info = self.env.step(1)
      # print(obs)
      # print(reward)
      # print(done)
    
    self.env.close()
