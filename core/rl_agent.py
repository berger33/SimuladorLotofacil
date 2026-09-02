import os
import random
import math
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

DQN_MODEL_FILE = "storage/dqn_model.pth"

# Espaço de Ações (Diferentes configurações do Motor)
ACOES = [
    {"nome": "Conservador Puro", "taxa_mutacao": 2, "severidade": 80, "apriori_ativo": False, "auto_piloto": False},
    {"nome": "Agressivo (Caos)", "taxa_mutacao": 15, "severidade": 10, "apriori_ativo": False, "auto_piloto": False},
    {"nome": "IA Preditiva Leve", "taxa_mutacao": 5, "severidade": 70, "apriori_ativo": True, "auto_piloto": True},
    {"nome": "Super Inteligência (Apriori+XGB)", "taxa_mutacao": 10, "severidade": 90, "apriori_ativo": True, "auto_piloto": True},
    {"nome": "Híbrido Mutante", "taxa_mutacao": 20, "severidade": 50, "apriori_ativo": True, "auto_piloto": False}
]

if TORCH_AVAILABLE:
    class DQNNetwork(nn.Module):
        def __init__(self, input_dim, output_dim):
            super(DQNNetwork, self).__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 64),
                nn.ReLU(),
                nn.Linear(64, output_dim)
            )

        def forward(self, x):
            return self.net(x)

    class ReplayBuffer:
        def __init__(self, capacity=10000):
            self.capacity = capacity
            self.buffer = []
            self.position = 0

        def push(self, state, action, reward, next_state):
            if len(self.buffer) < self.capacity:
                self.buffer.append(None)
            self.buffer[self.position] = (state, action, reward, next_state)
            self.position = (self.position + 1) % self.capacity

        def sample(self, batch_size):
            batch = random.sample(self.buffer, batch_size)
            state, action, reward, next_state = map(np.stack, zip(*batch))
            return state, action, reward, next_state

        def __len__(self):
            return len(self.buffer)

class RLAgent:
    def __init__(self, state_dim=5, gamma=0.99, epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=500, batch_size=32):
        self.action_dim = len(ACOES)
        self.state_dim = state_dim
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.steps_done = 0
        
        self.device = torch.device("cuda" if TORCH_AVAILABLE and torch.cuda.is_available() else "cpu")
        
        self.torch_ok = TORCH_AVAILABLE
        
        if self.torch_ok:
            self.policy_net = DQNNetwork(state_dim, self.action_dim).to(self.device)
            self.target_net = DQNNetwork(state_dim, self.action_dim).to(self.device)
            
            if os.path.exists(DQN_MODEL_FILE):
                try:
                    self.policy_net.load_state_dict(torch.load(DQN_MODEL_FILE, map_location=self.device, weights_only=True))
                    self.epsilon = self.epsilon_end # Já treinado, menos exploração aleatória
                except Exception:
                    pass
                    
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.target_net.eval()
            
            self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
            self.memory = ReplayBuffer(capacity=10000)
        
        self.estado_atual = np.zeros(self.state_dim)
        self.acao_atual_idx = 0
        self.ultima_acao = None
        
    def _save_model(self):
        if not self.torch_ok: return
        if not os.path.exists("storage"):
            os.makedirs("storage")
        torch.save(self.policy_net.state_dict(), DQN_MODEL_FILE)

    def determinar_estado(self, historico_media_pop, historico_h14, historico_h15, drawdown):
        """
        Retorna o vetor de estado (5 dimensões):
        [Tendência_Lucro, Drawdown, Taxa_14pts, Taxa_15pts, Volatilidade]
        """
        if len(historico_media_pop) < 5:
            return np.zeros(self.state_dim, dtype=np.float32)
            
        recentes_pop = historico_media_pop[-5:]
        tendencia = recentes_pop[-1] - recentes_pop[0]
        
        # Normalização simples
        tend_norm = np.clip(tendencia / 50.0, -1.0, 1.0)
        dd_norm = np.clip(drawdown / 1000.0, 0.0, 1.0)
        
        h14_ratio = (sum(historico_h14[-5:]) / 5.0) / 100.0 if len(historico_h14) >= 5 else 0.0
        h15_ratio = (sum(historico_h15[-5:]) / 5.0) / 10.0 if len(historico_h15) >= 5 else 0.0
        
        volatilidade = np.std(recentes_pop) / 20.0
        
        estado = np.array([tend_norm, dd_norm, h14_ratio, h15_ratio, volatilidade], dtype=np.float32)
        return estado

    def escolher_acao(self, estado):
        """Epsilon-greedy com Deep Neural Network"""
        if not self.torch_ok:
            self.acao_atual_idx = random.randint(0, len(ACOES) - 1)
            return ACOES[self.acao_atual_idx]
            
        self.epsilon = self.epsilon_end + (1.0 - self.epsilon_end) * math.exp(-1. * self.steps_done / self.epsilon_decay)
        self.steps_done += 1
        
        if random.random() < self.epsilon:
            self.acao_atual_idx = random.randint(0, len(ACOES) - 1)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(estado).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state_tensor)
                self.acao_atual_idx = q_values.argmax().item()
                
        self.estado_atual = estado
        self.ultima_acao = ACOES[self.acao_atual_idx]
        return self.ultima_acao

    def aprender(self, estado_anterior, acao_idx, recompensa, estado_novo):
        """Backpropagation no PyTorch usando Replay Memory"""
        if not self.torch_ok: return
        
        # Recompensa normalizada
        recompensa_norm = np.clip(recompensa / 50.0, -1.0, 1.0)
        
        self.memory.push(estado_anterior, acao_idx, recompensa_norm, estado_novo)
        
        if len(self.memory) < self.batch_size:
            return
            
        state_batch, action_batch, reward_batch, next_state_batch = self.memory.sample(self.batch_size)
        
        state_batch = torch.FloatTensor(state_batch).to(self.device)
        action_batch = torch.LongTensor(action_batch).unsqueeze(1).to(self.device)
        reward_batch = torch.FloatTensor(reward_batch).unsqueeze(1).to(self.device)
        next_state_batch = torch.FloatTensor(next_state_batch).to(self.device)
        
        # Current Q-values
        q_values = self.policy_net(state_batch).gather(1, action_batch)
        
        # Target Q-values
        with torch.no_grad():
            max_next_q_values = self.target_net(next_state_batch).max(1)[0].unsqueeze(1)
            target_q_values = reward_batch + (self.gamma * max_next_q_values)
            
        # Compute Loss
        loss = nn.MSELoss()(q_values, target_q_values)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient Clipping to prevent explosion
        for param in self.policy_net.parameters():
            if param.grad is not None:
                param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        
        # Update target network
        if self.steps_done % 100 == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self._save_model()
