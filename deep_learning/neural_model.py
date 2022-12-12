import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class LinearQNet(nn.Module):

  def __init__(self, n_observations, n_actions):
      super().__init__()
      self.layer1 = nn.Linear(n_observations, 10)
      self.layer2 = nn.Linear(10, 10)
      self.layer3 = nn.Linear(10, n_actions)

  # Called with either one element to determine next action, or a batch
  # during optimization. Returns tensor([[left0exp,right0exp]...]).
  def forward(self, x):
      x = F.relu(self.layer1(x))
      x = F.relu(self.layer2(x))
      return self.layer3(x)

class QTrainer:
  def __init__(self, learning_model, lr, gamma):
    self.learning_model = learning_model
    self.lr = lr
    self.gamma = gamma
    self.optimizer = optim.Adam(learning_model.parameters(), lr=lr)
    self.criterion = nn.MSELoss()

  def train_step(self, state, action, reward, next_state, done):
      state = torch.tensor(state, dtype=torch.float)
      next_state = torch.tensor(next_state, dtype=torch.float)
      action = torch.tensor(action, dtype=torch.long)
      reward = torch.tensor(reward, dtype=torch.float)
      # (n, x)

      if len(state.shape) == 1:
          # (1, x)
          state = torch.unsqueeze(state, 0)
          next_state = torch.unsqueeze(next_state, 0)
          action = torch.unsqueeze(action, 0)
          reward = torch.unsqueeze(reward, 0)
          done = (done, )

      # 1: predicted Q values with current state
      pred = self.model(state)

      target = pred.clone()
      for idx in range(len(done)):
          Q_new = reward[idx]
          if not done[idx]:
              Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

          target[idx][torch.argmax(action[idx]).item()] = Q_new
  
      # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
      # pred.clone()
      # preds[argmax(action)] = Q_new
      self.optimizer.zero_grad()
      loss = self.criterion(target, pred)
      loss.backward()

      self.optimizer.step()