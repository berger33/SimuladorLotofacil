"""
Atrasômetro - versão lite pura
"""
import math
from typing import List, Set, Dict, Tuple
from collections import Counter

def analisar_atrasos(sorteios: List[Set[int]]) -> Tuple[Dict[int, Dict], List[int]]:
    """
    Analisa atrasos de cada dezena.
    Retorna: (dados_finais, anomalias)
    dados_finais: {dezena: {"atual": int, "media": float, "limite": float, "status": str}}
    anomalias: lista dezenas prestes a estourar
    """
    atrasos_atuais = {i: 0 for i in range(1, 26)}
    atrasos_historicos = {i: [] for i in range(1, 26)}

    for sorteio in sorteios:
        for i in range(1, 26):
            if i in sorteio:
                atrasos_historicos[i].append(atrasos_atuais[i])
                atrasos_atuais[i] = 0
            else:
                atrasos_atuais[i] += 1

    dados_finais: Dict[int, Dict] = {}
    anomalias: List[int] = []

    for i in range(1, 26):
        historico = atrasos_historicos[i]
        if historico:
            media = sum(historico) / len(historico)
            variancia = sum((x - media) ** 2 for x in historico) / len(historico)
            desvio = math.sqrt(variancia)
        else:
            media, desvio = 0, 0

        limite_alerta = media + (desvio * 2)
        status = "NORMAL"

        if atrasos_atuais[i] >= limite_alerta and limite_alerta > 0:
            status = "ESTOURANDO"
            anomalias.append(i)

        dados_finais[i] = {
            "atual": atrasos_atuais[i],
            "media": media,
            "limite": limite_alerta,
            "status": status,
        }

    return dados_finais, anomalias

def gerar_relatorio_atrasometro(dados: Dict[int, Dict], anomalias: List[int]) -> str:
    texto = "📊 ESTATÍSTICA DE ATRASOS (Base Real DEDUPLICADA)\n\n"
    for n, d in sorted(dados.items()):
        texto += f"Dezena {n:02d} | Atual: {d['atual']:02d} | Média Hist: {d['media']:.1f} | Ruptura: {d['limite']:.1f} | {d['status']}\n"
    if anomalias:
        texto += f"\n🚨 ANOMALIAS DETECTADAS: {anomalias}\n"
    return texto
