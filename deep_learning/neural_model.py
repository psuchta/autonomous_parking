import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# https://github.com/ArchiMickey/QMario
# https://github.com/Chrispresso/SuperMarioBros-AI
# https://www.youtube.com/watch?v=WQ1bQAzBjPM
# https://www.youtube.com/watch?v=cyNPj-VNNkQ

# https://www.youtube.com/watch?v=rFwQDDbYTm4
# https://iopscience.iop.org/article/10.1088/1742-6596/1883/1/012111/pdf
# file:///Users/pawelsuchta/Downloads/Reinforcement_Learning-Based_Motion_Planning_for_A.pdf
# https://www.mathworks.com/help/reinforcement-learning/ug/train-ppo-agent-for-automatic-parking-valet.html
class LinearQNet(nn.Module):

  def __init__(self, n_observations, n_actions):
      super().__init__()
      self.layer1 = nn.Linear(n_observations, 30)
      self.layer2 = nn.Linear(30, 30)
      self.layer3 = nn.Linear(30, n_actions)

  # Called with either one element to determine next action, or a batch
  # during optimization. Returns tensor([[left0exp,right0exp]...]).
  def forward(self, x):
      x = F.relu(self.layer1(x))
      x = F.relu(self.layer2(x))
      return self.layer3(x)

  def save(self, file_name='model.pth'):
      model_folder_path = './neural_model'
      if not os.path.exists(model_folder_path):
          os.makedirs(model_folder_path)

      file_name = os.path.join(model_folder_path, file_name)
      torch.save(self.state_dict(), file_name)

class QTrainer:
  def __init__(self, learning_model, lr, gamma):
    self.learning_model = learning_model
    self.lr = lr
    self.gamma = gamma
    self.optimizer = optim.Adam(learning_model.parameters(), lr=lr)
    self.criterion = nn.MSELoss()
    # self.criterion = nn.SmoothL1Loss()

  def train_step(self, state, action, reward, next_state, done):
      # torch.tensor changes tuple ([1.2, 3.1], [4.1, 5.1]) into an object tensor([[1.2000, 3.1000],[4.1000, 5.1000]])
      # torch.tensor changes number 1.2 into an object tensor(1.200)
      state = torch.tensor(state, dtype=torch.float)
      next_state = torch.tensor(next_state, dtype=torch.float)
      action = torch.tensor(action, dtype=torch.long)
      reward = torch.tensor(reward, dtype=torch.float)
      # when sate hase one dimention (4,) or torch.Size([2])
      if len(state.shape) == 1:
          # (1, x)
          #unsqueeze(state, 0) converts [1, 2, 3, 4] -> [[ 1,  2,  3,  4]]
          # tensor(1.2000) -> tensor([1.2000])
          state = torch.unsqueeze(state, 0)
          next_state = torch.unsqueeze(next_state, 0)
          action = torch.unsqueeze(action, 0)
          reward = torch.unsqueeze(reward, 0)
          done = (done, )
      # pred CAN STORE MULTIPLE RESULT FOR DIFFERENT STATES
      # 1: predicted Q values with current state
      pred = self.learning_model(state)

      target = pred.clone()
      for idx in range(len(done)):
          Q_new = reward[idx]
          if not done[idx]:
              Q_new = reward[idx] + self.gamma * torch.max(self.learning_model(next_state[idx]))

          target[idx][torch.argmax(action[idx]).item()] = Q_new
  
      # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
      # pred.clone()
      # preds[argmax(action)] = Q_new
      self.optimizer.zero_grad()
      loss = self.criterion(target, pred)
      loss.backward()

      self.optimizer.step()
