import json
import os
import random
import time

QTABLE_FILE = "storage/rl_qtable.json"

# Espaço de Ações (Diferentes configurações do Motor)
ACOES = [
    {"nome": "Conservador Puro", "taxa_mutacao": 2, "severidade": 80, "apriori_ativo": False, "auto_piloto": False},
    {"nome": "Agressivo (Caos)", "taxa_mutacao": 15, "severidade": 10, "apriori_ativo": False, "auto_piloto": False},
    {"nome": "IA Preditiva Leve", "taxa_mutacao": 5, "severidade": 70, "apriori_ativo": True, "auto_piloto": True},
    {"nome": "Super Inteligência (Apriori+XGB)", "taxa_mutacao": 10, "severidade": 90, "apriori_ativo": True, "auto_piloto": True},
    {"nome": "Híbrido Mutante", "taxa_mutacao": 20, "severidade": 50, "apriori_ativo": True, "auto_piloto": False}
]

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto
        self.epsilon = epsilon  # Taxa de exploração
        self.q_table = self._load_qtable()
        self.estado_atual = "estagnado"
        self.acao_atual_idx = 0
        self.ultima_acao = None
        
    def _load_qtable(self):
        if os.path.exists(QTABLE_FILE):
            try:
                with open(QTABLE_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Inicializa a Q-table vazia se não existir
        # Estados: 'lucro', 'prejuizo', 'estagnado'
        q_t = {
            "lucro": [0.0] * len(ACOES),
            "prejuizo": [0.0] * len(ACOES),
            "estagnado": [0.0] * len(ACOES)
        }
        return q_t
        
    def _save_qtable(self):
        if not os.path.exists("storage"):
            os.makedirs("storage")
        with open(QTABLE_FILE, 'w') as f:
            json.dump(self.q_table, f, indent=4)

    def determinar_estado(self, historico_media_pop):
        """Define o estado do ambiente baseado no histórico recente (últimas 5 gerações)"""
        if len(historico_media_pop) < 5:
            return "estagnado"
            
        recentes = historico_media_pop[-5:]
        tendencia = recentes[-1] - recentes[0]
        
        if tendencia > 10.0:
            return "lucro"
        elif tendencia < -10.0:
            return "prejuizo"
        else:
            return "estagnado"

    def escolher_acao(self, estado):
        """Epsilon-greedy (Exploração vs Explotação)"""
        if random.uniform(0, 1) < self.epsilon:
            # Exploração: Escolhe uma ação aleatória
            self.acao_atual_idx = random.randint(0, len(ACOES) - 1)
        else:
            # Explotação: Escolhe a melhor ação para o estado atual
            valores_q = self.q_table.get(estado, [0.0] * len(ACOES))
            max_q = max(valores_q)
            melhores_indices = [i for i, v in enumerate(valores_q) if v == max_q]
            self.acao_atual_idx = random.choice(melhores_indices)
            
        self.estado_atual = estado
        self.ultima_acao = ACOES[self.acao_atual_idx]
        return self.ultima_acao

    def aprender(self, estado_anterior, acao_idx, recompensa, estado_novo):
        """Atualiza a Q-Table usando a Equação de Bellman"""
        q_anterior = self.q_table[estado_anterior][acao_idx]
        max_q_novo = max(self.q_table[estado_novo])
        
        # Q(s,a) = Q(s,a) + alpha * (R + gamma * max(Q(s',a')) - Q(s,a))
        novo_q = q_anterior + self.alpha * (recompensa + self.gamma * max_q_novo - q_anterior)
        self.q_table[estado_anterior][acao_idx] = novo_q
        self._save_qtable()
