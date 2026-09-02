from config import SOMA_MIN, SOMA_MAX, PRIMOS_ALVO, PARES_ALVO, MAX_SEQUENCIA

PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

def validar_jogo(jogo):
    nums = sorted(list(jogo))
    
    # 1. Soma
    soma = sum(nums)
    if not (SOMA_MIN <= soma <= SOMA_MAX):
        return False
        
    # 2. Primos
    qtd_primos = len([n for n in nums if n in PRIMOS])
    if qtd_primos not in PRIMOS_ALVO:
        return False
        
    # 3. Pares
    qtd_pares = len([n for n in nums if n % 2 == 0])
    if qtd_pares not in PARES_ALVO:
        return False
        
    # 4. Sequências
    seq_max = 1
    atual = 1
    for i in range(len(nums)-1):
        if nums[i+1] == nums[i] + 1:
            atual += 1
            seq_max = max(seq_max, atual)
        else:
            atual = 1
    if seq_max > MAX_SEQUENCIA:
        return False
        
    return True