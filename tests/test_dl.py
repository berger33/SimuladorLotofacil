import pytest
import numpy as np
import torch
from core.rl_agent import RLAgent, DQNNetwork, TORCH_AVAILABLE

@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch não está instalado")
def test_rl_agent_initialization():
    agent = RLAgent()
    assert agent.torch_ok is True
    assert isinstance(agent.policy_net, DQNNetwork)
    assert agent.state_dim == 5
    assert agent.action_dim == 5

@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch não está instalado")
def test_determinar_estado():
    agent = RLAgent()
    historico_pop = [10.0, 12.0, 15.0, 14.0, 20.0]
    historico_h14 = [1, 2, 0, 1, 3]
    historico_h15 = [0, 0, 0, 0, 1]
    drawdown = 50.0
    
    estado = agent.determinar_estado(historico_pop, historico_h14, historico_h15, drawdown)
    
    assert estado.shape == (5,)
    assert isinstance(estado, np.ndarray)
    assert estado.dtype == np.float32

@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch não está instalado")
def test_forward_pass():
    agent = RLAgent()
    estado = np.array([0.5, 0.1, 0.2, 0.0, 0.3], dtype=np.float32)
    
    acao = agent.escolher_acao(estado)
    assert acao is not None
    assert "taxa_mutacao" in acao
    assert "severidade" in acao

@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch não está instalado")
def test_aprender_batch():
    agent = RLAgent(batch_size=2)
    # Mockando a memória para forçar um batch de aprendizado rápido
    estado1 = np.zeros(5, dtype=np.float32)
    estado2 = np.ones(5, dtype=np.float32)
    
    agent.aprender(estado1, 0, 10.0, estado2)
    agent.aprender(estado2, 1, -5.0, estado1)
    
    assert len(agent.memory) == 2
    
    # O próximo aprender deve acionar o backpropagation (pois len >= batch_size)
    agent.aprender(estado1, 2, 5.0, estado2)
    assert len(agent.memory) == 3
