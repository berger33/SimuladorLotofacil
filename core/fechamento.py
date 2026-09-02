import random

def gerar_desdobramento(
    dezenas_20: set | list, 
    num_jogos: int, 
    tam_jogo: int, 
    filtros: dict | None = None
) -> list[list[int]]:
    
    if filtros is None:
        filtros = {}
        
    dezenas = sorted(list(dezenas_20))
    jogos_validos = []
    jogos_hashes = set()
    tentativas = 0
    
    impar_req = filtros.get("impar", False)
    moldura_req = filtros.get("moldura", False)
    primos_req = filtros.get("primos", False)
    
    primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    moldura_set = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    
    # Fase 1: Busca Estrita
    while len(jogos_validos) < num_jogos and tentativas < 5000:
        jogo_candidato = random.sample(dezenas, tam_jogo)
        jogo_candidato.sort()
        jogo_hash = tuple(jogo_candidato)
        tentativas += 1
        
        if jogo_hash in jogos_hashes: continue

        if impar_req and sum(1 for x in jogo_candidato if x % 2 != 0) not in [7, 8]: continue
        if moldura_req and sum(1 for x in jogo_candidato if x in moldura_set) not in [9, 10, 11]: continue
        if primos_req and sum(1 for x in jogo_candidato if x in primos_set) not in [4, 5, 6]: continue
            
        jogos_validos.append(jogo_candidato)
        jogos_hashes.add(jogo_hash)
            
    # Fase 2: Fallback com Relaxamento Gradual (Resolve o problema de jogos totalmente inválidos)
    relax_factor = 1
    while len(jogos_validos) < num_jogos:
        jogo_candidato = random.sample(dezenas, tam_jogo)
        jogo_candidato.sort()
        jogo_hash = tuple(jogo_candidato)
        
        if jogo_hash in jogos_hashes: continue
        
        if impar_req and sum(1 for x in jogo_candidato if x % 2 != 0) not in range(7-relax_factor, 8+relax_factor+1): 
            relax_factor += 1; continue
        if moldura_req and sum(1 for x in jogo_candidato if x in moldura_set) not in range(9-relax_factor, 11+relax_factor+1): 
            relax_factor += 1; continue
            
        jogos_validos.append(jogo_candidato)
        jogos_hashes.add(jogo_hash)
            
    return jogos_validos