from stable_baselines3.common.env_checker import check_env
from deep_learning.parking_env import ParkingEnv
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from gym.wrappers import TimeLimit
import os


class ParkLearning():
  def __init__(self):
    self.env = ParkingEnv()

  def simple_check(self):
    check_env(self.env)

  def random_check(self):
    while not self.env.can_close():
      obs = self.env.reset()
      done = False
      while not done and not self.env.can_close():
        action = self.env.action_space.sample()
        obs, reward, done, info = self.env.step(action)
    self.env.close()

  def obs_check(self):
    env = self.env
    obs = env.reset()
    done = False
    while not done:
      obs, reward, done, info = env.step([2])
      print(reward)
      print('*******')
      print(obs)
    env.close()

  def ppo_learning(self):
    logdir = f"deep_learning/tensorboard_logs/ppo_learning"
    env = self.__normalized_env()

    model = PPO('MlpPolicy', env, verbose = 1, ent_coef=0.02, tensorboard_log=logdir)
    # model = PPO('MlpPolicy', env, verbose = 1,learning_rate=0.0001, tensorboard_log=logdir)

    model.learn(total_timesteps=1000000)
    PPO_path = os.path.join('deep_learning', 'saved_models', 'PPO_model')
    model.save(PPO_path)

    # model.load(PPO_path)
    print('testing')
    self.__testing_loop(model, env)

  def dqn_learning(self):
    logdir = f"deep_learning/tensorboard_logs/dqn_learning"

    env = self.__normalized_env()
    model = DQN("MlpPolicy", env, verbose=1, learning_starts=100000, tensorboard_log=logdir)

    model.learn(total_timesteps=200000)
    PPO_path = os.path.join('deep_learning', 'saved_models', 'DQN_model')
    model.save(PPO_path)

    # model.load(PPO_path)
    print('testing')
    self.__testing_loop(model, env)

  def a2c_learning(self):
    logdir = f"deep_learning/tensorboard_logs/a2c_learning"
    env = self.__normalized_env()
    
    model = A2C("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
    model.learn(total_timesteps=100000)
    PPO_path = os.path.join('deep_learning', 'saved_models', 'A2C_model')
    model.save(PPO_path)
    
    # model.load(PPO_path)
    print('testing')
    self.__testing_loop(model, env)

  def __normalized_env(self):
    env = TimeLimit(self.env, max_episode_steps=700)
    env = Monitor(env)
    env = DummyVecEnv([lambda: env])
    env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=1., clip_reward=3.0)
    return env

  def __testing_loop(self, model, env):
    obs = self.env.reset()
    while True:
      action = model.predict(obs)
      obs, reward, done, info = env.step(action)
      if done:
        obs = env.reset()
