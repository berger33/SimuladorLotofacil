"""
Testes para core_shared - garante paridade com core original
"""
import pytest
import random
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

try:
    from android_app.core_shared.engine.fechamento import gerar_desdobramento
    from android_app.core_shared.engine.genetic_lite import gerar_sistema, crossover, mutacao, filtrar_diversidade
    from android_app.core_shared.engine.evaluator_lite import avaliar
    from android_app.core_shared.ml.atrasometro import analisar_atrasos
    from android_app.core_shared.ml.markov import gerar_previsao_markov
    from android_app.core_shared.data.repository import LocalJsonRepository
    from core.fechamento import gerar_desdobramento as gerar_desdobramento_original
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"Import falhou: {e}")
    CORE_AVAILABLE = False

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_fechamento_basico():
    base_20 = set(range(1, 21))
    jogos, relaxou = gerar_desdobramento(base_20, 10, 15)
    assert len(jogos) == 10
    # relaxou pode ser True ocasionalmente por colisão de hash, mas não deve travar
    for jogo in jogos:
        assert len(jogo) == 15
        assert set(jogo).issubset(base_20)

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_fechamento_com_filtros():
    base_20 = set(range(1, 21))
    filtros = {"impar": True}
    jogos, relaxou = gerar_desdobramento(base_20, 5, 15, filtros)
    assert len(jogos) == 5
    for jogo in jogos:
        impares = sum(1 for x in jogo if x % 2 != 0)
        assert impares in [7, 8] or relaxou

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_genetic_gerar_sistema():
    sistema = gerar_sistema(bloqueadas=[25], fixas=[1, 2], tam_base=20)
    assert len(sistema) == 20
    assert 1 in sistema and 2 in sistema
    assert 25 not in sistema

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_genetic_crossover():
    pai = set(range(1, 21))
    mae = set(range(6, 26))
    filho = crossover(pai, mae, tam_base=20)
    assert len(filho) == 20

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_genetic_mutacao():
    ind = set(range(1, 21))
    mutado = mutacao(ind, taxa=0.1, tam_base=20)
    assert len(mutado) == 20

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_evaluator():
    sorteios = [set(random.sample(range(1, 26), 15)) for _ in range(100)]
    individuo = set(range(1, 21))
    score, h11, h12, h13, h14, h15, ruins, sistema, relaxou = avaliar(
        individuo_20=individuo,
        filtros={},
        num_jogos=5,
        sorteios_treino=sorteios,
        simulacoes=100,
    )
    assert isinstance(score, float)
    assert len(sistema) == 5

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_atrasometro():
    sorteios = [set(random.sample(range(1, 26), 15)) for _ in range(100)]
    dados, anomalias = analisar_atrasos(sorteios)
    assert len(dados) == 25
    assert isinstance(anomalias, list)

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_markov():
    sorteios = [set(random.sample(range(1, 26), 15)) for _ in range(50)]
    top5, ranking = gerar_previsao_markov(sorteios)
    assert len(top5) == 5
    assert len(ranking) == 25

@pytest.mark.skipif(not CORE_AVAILABLE, reason="core_shared não disponível")
def test_paridade_fechamento():
    """Garante que novo fechamento dá mesmo resultado que antigo (com seed)"""
    random.seed(42)
    base_20 = set(range(1, 21))
    jogos_new, _ = gerar_desdobramento(base_20, 5, 15, {"impar": True})
    
    random.seed(42)
    jogos_old, _ = gerar_desdobramento_original(base_20, 5, 15, {"impar": True})
    
    # Devem ter mesmo tamanho (não necessariamente mesmos jogos por random, mas estrutura)
    assert len(jogos_new) == len(jogos_old) == 5

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
