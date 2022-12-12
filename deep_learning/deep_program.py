from base_program import BaseProgram
from deep_learning.neural_model import LinearQNet, QTrainer
from cars.autonomous_controlled_car import AutonomousControlledCar
from collections import deque
# from memory import ReplayMemory

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DeepProgram(BaseProgram):
  def __init__(self):
    self.memory = deque(maxlen=MAX_MEMORY) # popleft()
    self.model = LinearQNet(11, 4)
    self.gamma = 0.9
    self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    BaseProgram.__init__(self)

  def add_game_objects(self):
    car = None
    BaseProgram.add_game_objects(self)
    car = AutonomousControlledCar(700, 430, self.screen, self)
    self.add_car(car)

  def get_state(self, game):
    [

    ]

    return np.array(state, dtype=int)

  def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
        mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
    else:
        mini_sample = self.memory

    states, actions, rewards, next_states, dones = zip(*mini_sample)
    self.trainer.train_step(states, actions, rewards, next_states, dones)

  def train_short_memory(self, state, action, reward, next_state, done):
    self.trainer.train_step(state, action, reward, next_state, done)

  def get_action(self, state):
    # random moves: tradeoff exploration / exploitation
    self.epsilon = 80 - self.n_games
    final_move = [0,0,0]
    if random.randint(0, 200) < self.epsilon:
        move = random.randint(0, 2)
        final_move[move] = 1
    else:
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

    return final_move
