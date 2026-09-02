import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CACHE_FILE = "storage/resultados_historico_cache.json"

def baixar_resultados_reais() -> list[set[int]]:
    """
    Busca resultados reais de forma segura. 
    Prioriza APIs externas com Retry, e possui fallback para Cache Local.
    """
    # 1. Tenta carregar do Cache Local primeiro para extrema velocidade e offline support
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if dados and len(dados) > 1000:
                    return [set(sorteio) for sorteio in dados]
        except Exception:
            pass

    # 2. Configura resiliência de rede (Retry)
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # 3. Múltiplos endpoints de segurança
    endpoints = [
        "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil", # Oficial da Caixa
        "https://api.guidi.dev.br/loteria/lotofacil/ultimos",             # Alternativa estável
        "https://loteriascaixa-api.herokuapp.com/api/lotofacil"           # Fallback
    ]

    sorteios_processados = []

    for url in endpoints:
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                dados_brutos = response.json()
                
                # Tratamento depende do formato da API que responder primeiro
                if isinstance(dados_brutos, list):
                    for concurso in dados_brutos:
                        if "dezenas" in concurso:
                            dezenas = [int(d) for d in concurso["dezenas"]]
                            sorteios_processados.append(set(dezenas))
                            
                if sorteios_processados:
                    # 4. Salva no Cache para futuras inicializações
                    os.makedirs("storage", exist_ok=True)
                    with open(CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump([list(s) for s in sorteios_processados], f)
                    return sorteios_processados
                    
        except requests.exceptions.RequestException:
            continue # Tenta a próxima API se falhar

    # 5. Fallback Emergencial (Se tudo falhar e não houver cache)
    return []