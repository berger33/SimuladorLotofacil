import random
import math
from config import SIMULACOES, CUSTO_APOSTA, TAM_JOGO
from config import PREMIO_11, PREMIO_12, PREMIO_13, PREMIO_14, PREMIO_15
from core.crawler import baixar_resultados_reais
from core.fechamento import gerar_desdobramento

_WORKER_CACHE = {"treino": [], "validacao": [], "combos_ouro": []}

def _carregar_bases_seguras() -> tuple[list, list]:
    if not _WORKER_CACHE["treino"]:
        todos_sorteios = baixar_resultados_reais()
        if todos_sorteios and len(todos_sorteios) > 1000:
            corte = int(len(todos_sorteios) * 0.85)
            _WORKER_CACHE["treino"] = todos_sorteios[:corte]
            _WORKER_CACHE["validacao"] = todos_sorteios[corte:]
        else:
            _WORKER_CACHE["treino"] = [set(random.sample(range(1, 26), 15)) for _ in range(1000)]
            _WORKER_CACHE["validacao"] = [set(random.sample(range(1, 26), 15)) for _ in range(200)]
            
    return _WORKER_CACHE["treino"], _WORKER_CACHE["validacao"]

def avaliar(args: tuple) -> tuple:
    individuo_20, filtros, num_jogos, modo_treino, semente_ativa, foco_14, combos_ouro = args
    base_treino, _ = _carregar_bases_seguras()

    if semente_ativa:
        random.seed(42) 

    h11 = h12 = h13 = h14 = h15 = ruins = 0
    filtros_seguros = filtros if filtros is not None else {}
    sistema_jogos, relaxou = gerar_desdobramento(individuo_20, num_jogos, TAM_JOGO, filtros_seguros)
    
    sistema_jogos_sets = [set(j) for j in sistema_jogos]

    custo_por_sorteio = num_jogos * CUSTO_APOSTA
    retornos_simulacao = [] 

    for _ in range(SIMULACOES):
        if modo_treino == "Histórico" and base_treino:
            sorteio = random.choice(base_treino)
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
        
        lucro_deste_sorteio = faturamento_fitness - custo_por_sorteio
        retornos_simulacao.append(lucro_deste_sorteio)

    media_lucro = sum(retornos_simulacao) / SIMULACOES
    variancia = sum((r - media_lucro) ** 2 for r in retornos_simulacao) / SIMULACOES
    desvio_padrao = math.sqrt(variancia) if variancia > 0 else 1.0
    sharpe_ratio = media_lucro / desvio_padrao if desvio_padrao > 0 else 0
    
    bonus_apriori = 0
    if combos_ouro:
        for jogo_set in sistema_jogos_sets:
            for combo in combos_ouro:
                if combo.issubset(jogo_set):
                    bonus_apriori += 50

    score_final = media_lucro + (sharpe_ratio * 20) + bonus_apriori

    if semente_ativa: random.seed()

    return score_final, h11, h12, h13, h14, h15, ruins, sistema_jogos, relaxou