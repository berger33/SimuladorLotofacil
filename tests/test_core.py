import pytest
from core.fechamento import gerar_desdobramento

def test_gerar_desdobramento_basico():
    base_20 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
    num_jogos = 10
    tam_jogo = 15
    
    jogos, relaxou = gerar_desdobramento(base_20, num_jogos, tam_jogo)
    
    assert len(jogos) == num_jogos
    assert relaxou is False
    for jogo in jogos:
        assert len(jogo) == tam_jogo
        assert set(jogo).issubset(base_20)

def test_gerar_desdobramento_com_filtros():
    base_20 = set(range(1, 21))
    filtros = {"impar": True}
    
    jogos, relaxou = gerar_desdobramento(base_20, 5, 15, filtros)
    
    assert len(jogos) == 5
    for jogo in jogos:
        impares = sum(1 for x in jogo if x % 2 != 0)
        assert impares in [7, 8]