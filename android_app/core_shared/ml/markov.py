"""
Markov - Cadeias de Markov pura
"""
from typing import List, Set, Tuple, Dict

def gerar_previsao_markov(sorteios: List[Set[int]]) -> Tuple[List[int], List[Tuple[int, float]]]:
    """
    Gera previsão baseada em probabilidade condicional de transição.
    Retorna: (top_5, ranking_completo)
    """
    if len(sorteios) < 2:
        return [], []

    transicoes = {i: {j: 0 for j in range(1, 26)} for i in range(1, 26)}
    for t in range(1, len(sorteios)):
        for x in sorteios[t-1]:
            for y in sorteios[t]:
                transicoes[x][y] += 1

    probabilidades = {i: {} for i in range(1, 26)}
    for x, destinos in transicoes.items():
        total = sum(destinos.values())
        for y, count in destinos.items():
            probabilidades[x][y] = count / total if total > 0 else 0

    ultimo_sorteio = sorteios[-1]
    previsao_agregada = {i: 0.0 for i in range(1, 26)}

    for x in ultimo_sorteio:
        for y, prob in probabilidades[x].items():
            previsao_agregada[y] += prob

    dezenas_ordenadas = sorted(previsao_agregada.items(), key=lambda item: item[1], reverse=True)
    top_previsoes = [k for k, v in dezenas_ordenadas[:5]]
    return top_previsoes, dezenas_ordenadas

def gerar_relatorio_markov(ranking: List[Tuple[int, float]]) -> str:
    texto = "🔗 REDE DE MARKOV (Top Probabilidades de Transição)\n\n"
    for dezena, prob in ranking[:15]:
        texto += f"Dezena {dezena:02d} | Peso Condicional: {prob:.4f}\n"
    return texto
