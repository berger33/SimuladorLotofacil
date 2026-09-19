"""
Apriori - Mineração de trincas frequentes
"""
import itertools
from collections import Counter
from typing import List, Set

def minerar_regras_associacao(
    sorteios: List[Set[int]],
    top_n: int = 10,
    tamanho_combo: int = 3,
    janela: int = 500
) -> List[Set[int]]:
    """
    Minera combos frequentes nos últimos `janela` sorteios.
    Retorna lista de sets (trincas etc)
    """
    if not sorteios:
        return []

    sorteios_recentes = sorteios[-janela:] if len(sorteios) > janela else sorteios
    combos_freq = Counter()

    for sorteio in sorteios_recentes:
        dezenas = sorted(list(sorteio))
        for combo in itertools.combinations(dezenas, tamanho_combo):
            combos_freq[combo] += 1

    top_combos = [set(combo) for combo, count in combos_freq.most_common(top_n)]
    return top_combos

def gerar_relatorio_apriori(combos: List[Set[int]]) -> str:
    texto = f"💎 MINERAÇÃO APRIORI - {len(combos)} Combos de Ouro\n\n"
    for i, combo in enumerate(combos, 1):
        texto += f"{i:02d}. {sorted(list(combo))}\n"
    return texto
