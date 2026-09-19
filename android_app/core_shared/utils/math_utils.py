import math
from typing import List, Set
import random

def calcular_sharpe(retornos: List[float]) -> float:
    if not retornos:
        return 0.0
    media = sum(retornos) / len(retornos)
    variancia = sum((r - media) ** 2 for r in retornos) / len(retornos)
    desvio = math.sqrt(variancia) if variancia > 0 else 1.0
    return media / desvio if desvio > 0 else 0.0

def calcular_distancia_hamming(ind1: Set[int], ind2: Set[int]) -> int:
    return len(ind1.symmetric_difference(ind2))

def calcular_frequencia(sorteios: List[Set[int]]) -> dict:
    from collections import Counter
    freq = Counter()
    for s in sorteios:
        for n in s:
            freq[n] += 1
    return dict(freq)

def normalizar_scores(scores: dict) -> dict:
    if not scores:
        return {}
    max_score = max(scores.values()) if scores else 1
    if max_score == 0:
        return scores
    return {k: v / max_score for k, v in scores.items()}

def gerar_sorteio_aleatorio() -> Set[int]:
    return set(random.sample(range(1, 26), 15))

def calcular_soma(jogo: List[int]) -> int:
    return sum(jogo)

def contar_impares(jogo: List[int]) -> int:
    return sum(1 for x in jogo if x % 2 != 0)

def contar_primos(jogo: List[int]) -> int:
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    return sum(1 for x in jogo if x in primos)

def contar_moldura(jogo: List[int]) -> int:
    moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    return sum(1 for x in jogo if x in moldura)

def contar_fibonacci(jogo: List[int]) -> int:
    fibo = {1, 2, 3, 5, 8, 13, 21}
    return sum(1 for x in jogo if x in fibo)

def max_consecutiva(jogo: List[int]) -> int:
    if not jogo:
        return 0
    jogo_sorted = sorted(jogo)
    max_seq, atual = 1, 1
    for i in range(1, len(jogo_sorted)):
        if jogo_sorted[i] == jogo_sorted[i-1] + 1:
            atual += 1
            max_seq = max(max_seq, atual)
        else:
            atual = 1
    return max_seq
