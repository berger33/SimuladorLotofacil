import json
import os
from collections import Counter
from core.data import load

ARQUIVO_MEMORIA = "storage/memoria_pesos.json"

def inicializar_memoria():
    if not os.path.exists("storage"):
        os.makedirs("storage")
    if not os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump({"positiva": {}, "negativa": {}}, f)

def aprender():
    bons = load("melhores_matriz.json")
    freq = Counter()
    if bons:
        for item in bons:
            for n in item["base_20"]:
                freq[str(n)] += 3 
    return freq

def atualizar_memoria(melhor_individuo, memoria_ativa=True):
    if not memoria_ativa: return
    inicializar_memoria()
    with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
        mem = json.load(f)
    for n in melhor_individuo:
        chave = str(n)
        mem["positiva"][chave] = mem["positiva"].get(chave, 0) + 1
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mem, f)

def penalizar_jogo(pior_individuo, memoria_ativa=True):
    if not memoria_ativa: return
    inicializar_memoria()
    with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
        mem = json.load(f)
    for n in pior_individuo:
        chave = str(n)
        mem["negativa"][chave] = mem["negativa"].get(chave, 0) + 1
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mem, f)

def obter_pesos_memoria():
    inicializar_memoria()
    with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
        return json.load(f)