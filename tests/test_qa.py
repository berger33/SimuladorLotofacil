import pytest
from core.fechamento import gerar_desdobramento

@pytest.fixture
def base_20_ouro():
    return {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}

def test_desdobramento_sem_filtros_gera_33_jogos(base_20_ouro):
    jogos, relaxou = gerar_desdobramento(base_20_ouro, num_jogos=33, tam_jogo=15)
    assert len(jogos) == 33
    assert not relaxou
    for jogo in jogos:
        assert len(jogo) == 15

def test_filtro_impares_aplica_regra_corretamente(base_20_ouro):
    filtros = {"impar": True}
    jogos, relaxou = gerar_desdobramento(base_20_ouro, num_jogos=10, tam_jogo=15, filtros=filtros)
    
    for jogo in jogos:
        qtd_impares = sum(1 for n in jogo if n % 2 != 0)
        assert qtd_impares in (7, 8), f"Filtro falhou: Jogo gerado com {qtd_impares} ímpares."

def test_filtro_moldura_aplica_regra_corretamente(base_20_ouro):
    filtros = {"moldura": True}
    MOLDURA = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    jogos, relaxou = gerar_desdobramento(base_20_ouro, num_jogos=10, tam_jogo=15, filtros=filtros)
    
    for jogo in jogos:
        qtd_moldura = sum(1 for n in jogo if n in MOLDURA)
        assert qtd_moldura in (9, 10, 11), f"Filtro falhou: Jogo na moldura com {qtd_moldura}."