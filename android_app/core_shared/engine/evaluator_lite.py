"""
Evaluator Lite - versão desacoplada sem dependência de core/crawler global.
Recebe sorteios via injeção.
"""
import random
import math
from typing import List, Set, Dict, Tuple, Optional
from .fechamento import gerar_desdobramento

# Constantes padrão (podem vir de config)
CUSTO_APOSTA = 3.0
PREMIO_11 = 6.0
PREMIO_12 = 12.0
PREMIO_13 = 30.0
PREMIO_14 = 2000.0
PREMIO_15 = 600000.0
TAM_JOGO = 15
SIMULACOES_DEFAULT = 1000  # Mobile usa 1000, desktop 5000

def avaliar(
    individuo_20: Set[int],
    filtros: Dict,
    num_jogos: int,
    sorteios_treino: List[Set[int]],
    modo_treino: str = "Historico",
    foco_14: bool = False,
    combos_ouro: Optional[List[Set[int]]] = None,
    simulacoes: int = SIMULACOES_DEFAULT,
    tam_jogo: int = TAM_JOGO,
) -> Tuple[float, int, int, int, int, int, int, List[List[int]], bool]:
    """
    Avalia um indivíduo 20 dezenas.
    Retorna: score, h11, h12, h13, h14, h15, ruins, sistema_jogos, relaxou
    """
    h11 = h12 = h13 = h14 = h15 = ruins = 0
    filtros_seguros = filtros if filtros is not None else {}
    sistema_jogos, relaxou = gerar_desdobramento(individuo_20, num_jogos, tam_jogo, filtros_seguros)
    
    sistema_jogos_sets = [set(j) for j in sistema_jogos]

    custo_por_sorteio = num_jogos * CUSTO_APOSTA
    retornos_simulacao: List[float] = []

    for _ in range(simulacoes):
        if modo_treino == "Historico" and sorteios_treino:
            sorteio = random.choice(sorteios_treino)
        else:
            sorteio = set(random.sample(range(1, 26), 15))

        faturamento_fitness = 0
        for jogo_set in sistema_jogos_sets:
            acertos = len(jogo_set & sorteio)
            if acertos == 15:
                h15 += 1
                faturamento_fitness += (0 if foco_14 else PREMIO_15)
            elif acertos == 14:
                h14 += 1
                faturamento_fitness += PREMIO_14
            elif acertos == 13:
                h13 += 1
                faturamento_fitness += PREMIO_13
            elif acertos == 12:
                h12 += 1
                faturamento_fitness += PREMIO_12
            elif acertos == 11:
                h11 += 1
                faturamento_fitness += PREMIO_11
            else:
                ruins += 1
        
        lucro = faturamento_fitness - custo_por_sorteio
        retornos_simulacao.append(lucro)

    media_lucro = sum(retornos_simulacao) / simulacoes if simulacoes else 0
    variancia = sum((r - media_lucro) ** 2 for r in retornos_simulacao) / simulacoes if simulacoes else 0
    desvio_padrao = math.sqrt(variancia) if variancia > 0 else 1.0
    sharpe_ratio = media_lucro / desvio_padrao if desvio_padrao > 0 else 0
    
    bonus_apriori = 0
    if combos_ouro:
        for jogo_set in sistema_jogos_sets:
            for combo in combos_ouro:
                if combo.issubset(jogo_set):
                    bonus_apriori += 50

    score_final = media_lucro + (sharpe_ratio * 20) + bonus_apriori

    return score_final, h11, h12, h13, h14, h15, ruins, sistema_jogos, relaxou

def avaliar_para_api(args: Tuple) -> Tuple:
    """
    Wrapper compatível com ProcessPoolExecutor.map
    args: (individuo_20, filtros, num_jogos, sorteios_treino, modo_treino, foco_14, combos_ouro, simulacoes)
    """
    individuo_20, filtros, num_jogos, sorteios_treino, modo_treino, foco_14, combos_ouro, simulacoes = args
    return avaliar(
        individuo_20=individuo_20,
        filtros=filtros,
        num_jogos=num_jogos,
        sorteios_treino=sorteios_treino,
        modo_treino=modo_treino,
        foco_14=foco_14,
        combos_ouro=combos_ouro,
        simulacoes=simulacoes,
    )

def stress_test(
    sistema_jogos: List[List[int]],
    sorteios: List[Set[int]],
    tipo: str = "historico"
) -> Dict:
    """
    Prova de fogo: testa sistema contra sorteios reais ou caos.
    """
    h11 = h12 = h13 = h14 = h15 = ruins = 0
    qtd_testes = len(sorteios)
    custo_total = qtd_testes * len(sistema_jogos) * CUSTO_APOSTA

    for sorteio in sorteios:
        for jogo in sistema_jogos:
            acertos = len(set(jogo) & sorteio)
            if acertos == 15:
                h15 += 1
            elif acertos == 14:
                h14 += 1
            elif acertos == 13:
                h13 += 1
            elif acertos == 12:
                h12 += 1
            elif acertos == 11:
                h11 += 1
            else:
                ruins += 1

    faturamento = (h11 * PREMIO_11) + (h12 * PREMIO_12) + (h13 * PREMIO_13) + (h14 * PREMIO_14) + (h15 * PREMIO_15)
    lucro = faturamento - custo_total
    roi = (lucro / custo_total) * 100 if custo_total > 0 else 0

    return {
        "tipo": tipo,
        "qtd_testes": qtd_testes,
        "lucro": lucro,
        "roi": roi,
        "h11": h11,
        "h12": h12,
        "h13": h13,
        "h14": h14,
        "h15": h15,
        "ruins": ruins,
        "faturamento": faturamento,
        "custo_total": custo_total,
    }
