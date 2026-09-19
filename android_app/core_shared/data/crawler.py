"""
Crawler resiliente com 3 endpoints + cache + User-Agent
Versão lite sem requests obrigatório? Usa requests se disponível
"""
import json
import os
from typing import List, Set

CACHE_FILE_DEFAULT = "storage/resultados_historico_cache.json"

def baixar_resultados_reais(cache_file: str = CACHE_FILE_DEFAULT) -> List[Set[int]]:
    # 1. Tenta cache local primeiro
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if dados and len(dados) > 100:
                    return [set(s) for s in dados]
        except Exception:
            pass

    # 2. Tenta requests
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        endpoints = [
            "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil",
            "https://api.guidi.dev.br/loteria/lotofacil/ultimos",
            "https://loteriascaixa-api.herokuapp.com/api/lotofacil"
        ]

        for url in endpoints:
            try:
                response = session.get(url, timeout=10, headers={
                    "User-Agent": "LotofacilPro/1.0 (Educational; +https://github.com/berger33/SimuladorLotofacil)"
                })
                if response.status_code == 200:
                    dados_brutos = response.json()
                    sorteios = []
                    if isinstance(dados_brutos, list):
                        for concurso in dados_brutos:
                            if "dezenas" in concurso:
                                dezenas = [int(d) for d in concurso["dezenas"]]
                                sorteios.append(set(dezenas))
                    if sorteios:
                        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                        with open(cache_file, "w", encoding="utf-8") as f:
                            json.dump([list(s) for s in sorteios], f)
                        return sorteios
            except Exception:
                continue
    except ImportError:
        pass

    # 3. Fallback vazio
    return []

# Alias para compatibilidade
def carregar_sorteios_com_fallback(cache_file: str = CACHE_FILE_DEFAULT) -> List[Set[int]]:
    sorteios = baixar_resultados_reais(cache_file)
    if not sorteios:
        import random
        return [set(random.sample(range(1, 26), 15)) for _ in range(1000)]
    return sorteios
