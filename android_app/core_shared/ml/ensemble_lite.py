"""
Ensemble Lite - sem dependência obrigatória de XGBoost
Se XGBoost disponível, usa. Se não, fallback para média móvel + Markov + Atraso
"""
from typing import List, Set, Tuple, Dict
import math
from .atrasometro import analisar_atrasos
from .markov import gerar_previsao_markov

try:
    import xgboost as xgb
    import numpy as np
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None
    np = None

def executar_ensemble_hibrido(
    sorteios: List[Set[int]],
    usar_xgboost: bool = True,
    top_n: int = 5
) -> Tuple[List[int], str]:
    """
    Ensemble Híbrido: 40% Markov + 20% Atraso + 40% XGBoost (ou fallback)
    Retorna: (top_5, relatorio)
    """
    pontuacao_final = {i: 0.0 for i in range(1, 26)}
    logs: List[str] = []

    # 1. Markov 40%
    top_markov, markov_probs = gerar_previsao_markov(sorteios)
    max_markov = max(p for _, p in markov_probs) if markov_probs else 1.0
    for dezena, prob in markov_probs:
        pontuacao_final[dezena] += (prob / max_markov) * 40.0 if max_markov > 0 else 0

    # 2. Atraso 20%
    dados_atraso, _ = analisar_atrasos(sorteios)
    max_atraso = max(d['atual'] for d in dados_atraso.values()) if dados_atraso else 1.0
    for dezena, info in dados_atraso.items():
        ratio = info['atual'] / max_atraso if max_atraso > 0 else 0
        pontuacao_final[dezena] += ratio * 20.0

    # 3. XGBoost 40% ou fallback
    if usar_xgboost and XGBOOST_AVAILABLE and len(sorteios) > 10:
        try:
            # Últimos 300 sorteios
            sorteios_rec = sorteios[-300:]
            X, y = [], {i: [] for i in range(1, 26)}

            for t in range(1, len(sorteios_rec) - 1):
                row = [1 if n in sorteios_rec[t-1] else 0 for n in range(1, 26)]
                X.append(row)
                for n in range(1, 26):
                    y[n].append(1 if n in sorteios_rec[t] else 0)

            X_np = np.array(X)
            latest = np.array([[1 if n in sorteios_rec[-1] else 0 for n in range(1, 26)]])

            for n in range(1, 26):
                y_n = np.array(y[n])
                if len(set(y_n)) > 1:  # variação
                    model = xgb.XGBClassifier(eval_metric='logloss', max_depth=3, n_estimators=20, verbosity=0)
                    model.fit(X_np, y_n)
                    prob = model.predict_proba(latest)[0][1]
                    pontuacao_final[n] += prob * 40.0

            logs.append("✅ XGBoost: Árvores injetadas com sucesso!")
        except Exception as e:
            logs.append(f"⚠️ XGBoost falhou ({e}), usando fallback")
            # Fallback: distribui 40% proporcional a frequência
            from collections import Counter
            freq = Counter()
            for s in sorteios[-100:]:
                for n in s:
                    freq[n] += 1
            max_freq = max(freq.values()) if freq else 1
            for n in range(1, 26):
                pontuacao_final[n] += (freq.get(n, 0) / max_freq) * 40.0
    else:
        if not XGBOOST_AVAILABLE:
            logs.append("⚠️ XGBoost não disponível, usando frequência como fallback")
        # Fallback frequência
        from collections import Counter
        freq = Counter()
        for s in sorteios[-100:]:
            for n in s:
                freq[n] += 1
        max_freq = max(freq.values()) if freq else 1
        for n in range(1, 26):
            pontuacao_final[n] += (freq.get(n, 0) / max_freq) * 40.0
        if XGBOOST_AVAILABLE:
            logs.append("✅ Fallback frequência aplicado")

    ranking = sorted(pontuacao_final.items(), key=lambda x: x[1], reverse=True)
    top_5 = [k for k, v in ranking[:top_n]]

    relatorio = "🏆 CONSELHO JEDI: ENSEMBLE HÍBRIDO (XGBoost + Markov + Atraso)\n\n"
    for msg in logs:
        relatorio += f"{msg}\n"
    relatorio += "\nDezena | Score IA (0-100)\n" + "-"*40 + "\n"
    for dezena, score in ranking[:15]:
        relatorio += f"[{dezena:02d}] | ⭐ {score:.2f} pts\n"

    return top_5, relatorio
