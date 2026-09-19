"""
Genetic Lite - Versão desacoplada sem dependência de UI, storage global ou customtkinter.
Mantém mesma lógica do core/genetic.py mas com injeção de dependência.
"""
import random
from collections import Counter
from typing import List, Set, Dict, Optional

TAM_BASE_DEFAULT = 20

def get_validas(bloqueadas: Optional[List[int]] = None, fixas: Optional[List[int]] = None) -> List[int]:
    todas = set(range(1, 26))
    if bloqueadas:
        todas -= set(bloqueadas)
    if fixas:
        todas -= set(fixas)
    return list(todas)

def gerar_individuo(
    freq_dict: Optional[Dict[str, int]] = None,
    bloqueadas: Optional[List[int]] = None,
    fixas: Optional[List[int]] = None,
    severidade: float = 1.0,
    memoria_ativa: bool = True,
    tam_base: int = TAM_BASE_DEFAULT,
) -> Set[int]:
    validas = get_validas(bloqueadas, fixas)
    individuo = set(fixas) if fixas else set()

    pool: List[int] = []
    if memoria_ativa and freq_dict:
        for num in validas:
            peso = 1 + int(freq_dict.get(str(num), 0) * (1.0 - severidade))
            pool.extend([num] * max(1, peso))
    else:
        pool = validas.copy()

    attempts = 0
    while len(individuo) < tam_base and attempts < 1000:
        if pool:
            escolha = random.choice(pool)
            if escolha not in individuo:
                individuo.add(escolha)
        attempts += 1

    while len(individuo) < tam_base:
        individuo.add(random.choice(validas))

    return individuo

def gerar_sistema(
    memoria_pesos: Optional[Dict[str, int]] = None,
    bloqueadas: Optional[List[int]] = None,
    fixas: Optional[List[int]] = None,
    severidade: float = 1.0,
    memoria_ativa: bool = True,
    tam_base: int = TAM_BASE_DEFAULT,
) -> Set[int]:
    freq = Counter()
    if memoria_pesos:
        for k, v in memoria_pesos.items():
            freq[k] = v
    return gerar_individuo(freq, bloqueadas, fixas, severidade, memoria_ativa, tam_base)

def crossover(
    pai: Set[int],
    mae: Set[int],
    bloqueadas: Optional[List[int]] = None,
    fixas: Optional[List[int]] = None,
    tam_base: int = TAM_BASE_DEFAULT,
) -> Set[int]:
    l1, l2 = list(pai), list(mae)
    random.shuffle(l1)
    random.shuffle(l2)

    novo = set(fixas) if fixas else set()
    for n in l1 + l2:
        if len(novo) < tam_base and n not in (bloqueadas or []):
            novo.add(n)

    validas = get_validas(bloqueadas, fixas)
    while len(novo) < tam_base:
        novo.add(random.choice(validas))
    return novo

def mutacao(
    individuo: Set[int],
    taxa: float,
    bloqueadas: Optional[List[int]] = None,
    fixas: Optional[List[int]] = None,
    tam_base: int = TAM_BASE_DEFAULT,
) -> Set[int]:
    novo = set(individuo)
    validas = get_validas(bloqueadas, fixas)

    for _ in range(len(novo)):
        if random.random() < taxa:
            removivel = list(novo - set(fixas or []))
            if removivel:
                novo.remove(random.choice(removivel))
                while len(novo) < tam_base:
                    novo.add(random.choice(validas))
    return novo

def calcular_distancia_hamming(ind1: Set[int], ind2: Set[int]) -> int:
    return len(ind1.symmetric_difference(ind2))

def filtrar_diversidade(
    populacao: List[Set[int]],
    novo_ind: Set[int],
    tolerancia: float = 0.85,
    usar_hamming: bool = False,
    tam_base: int = TAM_BASE_DEFAULT,
) -> bool:
    if usar_hamming:
        distancia_minima = int(tam_base * (1.0 - tolerancia)) * 2
        for ind in populacao:
            if calcular_distancia_hamming(ind, novo_ind) < distancia_minima:
                return False
        return True
    else:
        for ind in populacao:
            intersecao = len(ind & novo_ind)
            if intersecao / tam_base >= tolerancia:
                return False
        return True
