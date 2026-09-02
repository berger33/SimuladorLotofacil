import random
from collections import Counter
from config import TAM_BASE
from core.data import load

def get_validas(bloqueadas=None, fixas=None):
    todas = set(range(1, 26))
    if bloqueadas:
        todas -= set(bloqueadas)
    if fixas:
        todas -= set(fixas)
    return list(todas)

def gerar_individuo(freq_dict=None, bloqueadas=None, fixas=None, severidade=1.0, memoria_ativa=True):
    validas = get_validas(bloqueadas, fixas)
    individuo = set(fixas) if fixas else set()
    
    pool = []
    if memoria_ativa and freq_dict:
        for num in validas:
            peso = 1 + int(freq_dict.get(str(num), 0) * (1.0 - severidade)) 
            pool.extend([num] * max(1, peso))
    else:
        pool = validas.copy()

    while len(individuo) < TAM_BASE:
        if pool:
            escolha = random.choice(pool)
            if escolha not in individuo:
                individuo.add(escolha)
        else:
            break
            
    while len(individuo) < TAM_BASE:
        individuo.add(random.choice(validas))
        
    return individuo

def gerar_sistema(bloqueadas=None, fixas=None, severidade=1.0, memoria_ativa=True, num_jogos=33):
    bons = load(f"melhores_matriz_{num_jogos}.json")
    freq = Counter()
    if bons:
        for item in bons:
            for n in item["base_20"]:
                freq[str(n)] += 1
    return gerar_individuo(freq, bloqueadas, fixas, severidade, memoria_ativa)

def crossover(pai, mae, bloqueadas=None, fixas=None):
    l1, l2 = list(pai), list(mae)
    random.shuffle(l1)
    random.shuffle(l2)
    
    novo = set(fixas) if fixas else set()
    for n in l1 + l2:
        if len(novo) < TAM_BASE and n not in (bloqueadas or []):
            novo.add(n)
            
    validas = get_validas(bloqueadas, fixas)
    while len(novo) < TAM_BASE:
        novo.add(random.choice(validas))
    return novo

def mutacao(individuo, taxa, bloqueadas=None, fixas=None):
    novo = set(individuo)
    validas = get_validas(bloqueadas, fixas)
    
    for _ in range(len(novo)):
        if random.random() < taxa:
            removivel = list(novo - set(fixas or []))
            if removivel:
                novo.remove(random.choice(removivel))
                while len(novo) < TAM_BASE:
                    novo.add(random.choice(validas))
    return novo

# --- ETAPA 3: MÉTRICA AVANÇADA DE DIVERSIDADE ---
def calcular_distancia_hamming(ind1, ind2):
    """Mede a diferença absoluta entre dois genomas (Symmetric Difference)"""
    return len(ind1.symmetric_difference(ind2))

def filtrar_diversidade(populacao, novo_ind, tolerancia=0.85, usar_hamming=False):
    """
    Filtra clones para garantir cobertura combinatória real.
    """
    if usar_hamming:
        # Pelo menos X dezenas diferentes absolutas baseadas na tolerância
        distancia_minima = int(TAM_BASE * (1.0 - tolerancia)) * 2 
        for ind in populacao:
            if calcular_distancia_hamming(ind, novo_ind) < distancia_minima:
                return False
        return True
    else:
        # Heurística antiga
        for ind in populacao:
            intersecao = len(ind & novo_ind)
            if intersecao / TAM_BASE >= tolerancia:
                return False
        return True