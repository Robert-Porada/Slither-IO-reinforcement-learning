import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os 


class Linear_Qnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x
    
    def save(self, filename="model.pth"):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, filename)
        torch.save(self.state_dict(), file_name)
    
    def load(self, filepath="./model/model.pth"):
        self.load_state_dict(torch.load(filepath))
        self.eval()

class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.loss = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        # Simplified bellman equasion
        # 1. Predicted q values with current statte
        pred = self.model(state)
        # print("q pred ", pred)

        target = pred.clone()
        for i in range(len(state)):
            Q_new = reward[i]
            # print("Q_new", Q_new)
            if not game_over[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
                # print("Qnew", Q_new)
            target[i][torch.argmax(action).item()] = Q_new
        # print("target", target)

        # 2. q_new = r + y * max(next_predicted q value) --> only if not game over
        # pred.clone()
        # preds[argmax(actoon)] = q_new
        self.optimizer.zero_grad()
        # print("target", target, "pred", pred)
        loss = self.loss(target, pred)
        loss.backward()
        self.optimizer.step()