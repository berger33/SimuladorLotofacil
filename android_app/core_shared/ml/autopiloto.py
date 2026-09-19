"""
Auto-Piloto - Prevê macro propriedades (soma, ímpares, etc) para próximo sorteio
Usa XGBoost Regressor se disponível, senão média móvel ponderada
"""
from typing import List, Set, Dict

def prever_macro_propriedades(sorteios: List[Set[int]]) -> Dict[str, int]:
    """
    Prevê soma, ímpares, moldura, primos, fibonacci para próximo sorteio
    """
    if len(sorteios) < 50:
        return {}

    primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    moldura_set = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    fibo_set = {1, 2, 3, 5, 8, 13, 21}

    def get_macros(sorteio: Set[int]) -> Dict[str, int]:
        s_list = list(sorteio)
        return {
            "impar": sum(1 for x in s_list if x % 2 != 0),
            "moldura": sum(1 for x in s_list if x in moldura_set),
            "primos": sum(1 for x in s_list if x in primos_set),
            "fibonacci": sum(1 for x in s_list if x in fibo_set),
            "soma": sum(s_list),
        }

    historico_macros = [get_macros(s) for s in sorteios[-300:]]

    previsoes: Dict[str, int] = {}

    try:
        import xgboost as xgb
        import numpy as np

        for feature in ["impar", "moldura", "primos", "fibonacci", "soma"]:
            y = [h[feature] for h in historico_macros]
            X, y_target = [], []
            for i in range(3, len(y)):
                X.append([y[i-3], y[i-2], y[i-1]])
                y_target.append(y[i])

            if len(X) < 10:
                continue

            model = xgb.XGBRegressor(n_estimators=30, max_depth=3, objective='reg:squarederror', verbosity=0)
            model.fit(np.array(X), np.array(y_target))

            last_3 = np.array([[y[-3], y[-2], y[-1]]])
            pred = model.predict(last_3)[0]
            previsoes[feature] = int(round(pred))

    except ImportError:
        # Fallback WMA
        for feature in ["impar", "moldura", "primos", "fibonacci", "soma"]:
            y = [h[feature] for h in historico_macros[-10:]]
            weights = list(range(1, 11))
            wma = sum(y[i]*weights[i] for i in range(min(10, len(y)))) / sum(weights[:len(y)])
            previsoes[feature] = int(round(wma))

    return previsoes

def gerar_relatorio_autopiloto(previsoes: Dict[str, int]) -> str:
    if not previsoes:
        return "Auto-Piloto: dados insuficientes"
    texto = "🎯 AUTO-PILOTO - Alvos previstos para próximo sorteio:\n\n"
    for k, v in previsoes.items():
        texto += f"{k}: {v}\n"
    return texto
