import math
import itertools
from collections import Counter
from core.evaluator import _carregar_bases_seguras

def minerar_regras_associacao(top_n=10, tamanho_combo=3):
    treino, validacao = _carregar_bases_seguras()
    sorteios = treino + validacao
    
    if not sorteios: return []
        
    combos_freq = Counter()
    sorteios_recentes = sorteios[-500:] # Otimização: analisar apenas histórico recente
    
    for sorteio in sorteios_recentes:
        dezenas = sorted(list(sorteio))
        para_combos = list(itertools.combinations(dezenas, tamanho_combo))
        for combo in para_combos:
            combos_freq[combo] += 1
            
    top_combos = [set(combo) for combo, count in combos_freq.most_common(top_n)]
    return top_combos

def prever_macro_propriedades():
    """
    Usa XGBoost Regressor (se disponível) ou Média Móvel para prever 
    o alvo exato dos filtros (Soma, Ímpares, Moldura, etc) para o próximo sorteio.
    """
    treino, validacao = _carregar_bases_seguras()
    sorteios = treino + validacao
    if len(sorteios) < 50: return {}
    
    primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    moldura_set = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    fibo_set = {1, 2, 3, 5, 8, 13, 21}
    
    def get_macros(sorteio):
        s_list = list(sorteio)
        impar = sum(1 for x in s_list if x % 2 != 0)
        mold = sum(1 for x in s_list if x in moldura_set)
        prim = sum(1 for x in s_list if x in primos_set)
        fibo = sum(1 for x in s_list if x in fibo_set)
        soma = sum(s_list)
        return {"impar": impar, "moldura": mold, "primos": prim, "fibonacci": fibo, "soma": soma}
        
    historico_macros = [get_macros(s) for s in sorteios[-300:]] # ultimos 300
    
    previsoes = {}
    try:
        import xgboost as xgb
        import numpy as np
        
        for feature in ["impar", "moldura", "primos", "fibonacci", "soma"]:
            y = [h[feature] for h in historico_macros]
            # Criar lags de 3 periodos
            X, y_target = [], []
            for i in range(3, len(y)):
                X.append([y[i-3], y[i-2], y[i-1]])
                y_target.append(y[i])
                
            model = xgb.XGBRegressor(n_estimators=30, max_depth=3, objective='reg:squarederror')
            model.fit(np.array(X), np.array(y_target))
            
            # Prever o proximo
            last_3 = np.array([[y[-3], y[-2], y[-1]]])
            pred = model.predict(last_3)[0]
            previsoes[feature] = int(round(pred))
    except ImportError:
        # Fallback para Média Móvel Exponencial (EMA) rápida
        for feature in ["impar", "moldura", "primos", "fibonacci", "soma"]:
            y = [h[feature] for h in historico_macros[-10:]]
            weights = list(range(1, 11))
            wma = sum(y[i]*weights[i] for i in range(10)) / sum(weights)
            previsoes[feature] = int(round(wma))
            
    return previsoes

def analisar_atrasos():
    treino, validacao = _carregar_bases_seguras()
    sorteios = treino + validacao
    
    atrasos_atuais = {i: 0 for i in range(1, 26)}
    atrasos_historicos = {i: [] for i in range(1, 26)}
    
    for sorteio in sorteios:
        for i in range(1, 26):
            if i in sorteio:
                atrasos_historicos[i].append(atrasos_atuais[i])
                atrasos_atuais[i] = 0
            else:
                atrasos_atuais[i] += 1
                
    dados_finais = {}
    anomalias = []
    
    for i in range(1, 26):
        historico = atrasos_historicos[i]
        if historico:
            media = sum(historico) / len(historico)
            variancia = sum((x - media)**2 for x in historico) / len(historico)
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
            "status": status
        }
        
    return dados_finais, anomalias

def gerar_previsao_markov():
    treino, validacao = _carregar_bases_seguras()
    sorteios = treino + validacao
    
    if len(sorteios) < 2: return [], []
        
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

def executar_ensemble_hibrido():
    """
    ETAPA 4: ENSEMBLE HÍBRIDO.
    Pondera Heurística (Atraso) + Markov + XGBoost.
    """
    pontuacao_final = {i: 0.0 for i in range(1, 26)}
    logs = []

    # 1. Componente de Markov (Peso: 40%)
    _, markov_probs = gerar_previsao_markov()
    max_markov = max(p for _, p in markov_probs) if markov_probs else 1.0
    for dezena, prob in markov_probs:
        pontuacao_final[dezena] += (prob / max_markov) * 40.0 if max_markov > 0 else 0

    # 2. Componente de Atraso (Peso: 20%)
    dados_atraso, _ = analisar_atrasos()
    max_atraso = max(d['atual'] for d in dados_atraso.values()) if dados_atraso else 1.0
    for dezena, info in dados_atraso.items():
        ratio_atraso = info['atual'] / max_atraso if max_atraso > 0 else 0
        pontuacao_final[dezena] += ratio_atraso * 20.0

    # 3. Componente Machine Learning Avançado (XGBoost) (Peso: 40%)
    xgboost_ok = False
    try:
        import xgboost as xgb
        import numpy as np
        xgboost_ok = True
    except ImportError:
        logs.append("⚠️ XGBoost não detetado. Correndo apenas com Markov + Atrasos.")
        logs.append("Para ativar a Força Total, corra no terminal: pip install xgboost numpy")

    if xgboost_ok:
        treino, _ = _carregar_bases_seguras()
        if len(treino) > 10:
            sorteios = treino[-300:] # Últimos 300 sorteios para ser rápido
            X, y = [], {i: [] for i in range(1, 26)}
            
            for t in range(1, len(sorteios) - 1):
                row = [1 if n in sorteios[t-1] else 0 for n in range(1, 26)]
                X.append(row)
                for n in range(1, 26):
                    y[n].append(1 if n in sorteios[t] else 0)
            
            X = np.array(X)
            feature_latest = np.array([[1 if n in sorteios[-1] else 0 for n in range(1, 26)]])
            
            for n in range(1, 26):
                y_n = np.array(y[n])
                if len(np.unique(y_n)) > 1: # Só treina se a dezena teve variação
                    model = xgb.XGBClassifier(eval_metric='logloss', max_depth=3, n_estimators=20)
                    model.fit(X, y_n)
                    prob = model.predict_proba(feature_latest)[0][1]
                    pontuacao_final[n] += prob * 40.0
        logs.append("✅ XGBoost: Árvores de Decisão injetadas no Ensemble com Sucesso!")

    # Ordenar e eleger o "Conselho" (Top 5 Dezenas de Ouro)
    ranking = sorted(pontuacao_final.items(), key=lambda item: item[1], reverse=True)
    top_5 = [k for k, v in ranking[:5]]
    
    relatorio = "🏆 O CONSELHO JEDI: ENSEMBLE HÍBRIDO (XGBoost + Markov + Atraso)\n\n"
    for msg in logs: relatorio += f"{msg}\n"
    relatorio += "\nDezena | Score de Confiança da Inteligência Artificial (0 a 100)\n"
    relatorio += "-"*65 + "\n"
    for dezena, score in ranking[:15]:
        relatorio += f"[{dezena:02d}]   | ⭐ {score:.2f} pts\n"

    return top_5, relatorio