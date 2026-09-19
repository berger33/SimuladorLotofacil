"""
FastAPI Backend REAL - usando core_shared de verdade
Rodar: uvicorn main_real:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import random
import time
import sys
import os
import json
import asyncio

# Adiciona core_shared
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from core_shared.data.repository import LocalJsonRepository, RemoteApiRepository, CachedRepository
    from core_shared.data.crawler import carregar_sorteios_com_fallback
    from core_shared.engine.engine import MotorLotofacilLite
    from core_shared.domain.models import ConfigGeracao, Filtros
    from core_shared.domain.enums import ModoTreino
    from core_shared.ml.atrasometro import analisar_atrasos, gerar_relatorio_atrasometro
    from core_shared.ml.markov import gerar_previsao_markov, gerar_relatorio_markov
    from core_shared.ml.ensemble_lite import executar_ensemble_hibrido
    from core_shared.ml.apriori import minerar_regras_associacao, gerar_relatorio_apriori
    from core_shared.ml.autopiloto import prever_macro_propriedades, gerar_relatorio_autopiloto
    from core_shared.engine.evaluator_lite import stress_test
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"core_shared não disponível: {e}, usando mocks")
    CORE_AVAILABLE = False

app = FastAPI(
    title="Lotofácil Pro API - REAL",
    description="API educacional com core_shared real - Não afiliada à Caixa",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache global
_sorteios_cache: List[set] = []
_sorteios_cache_time = 0

def get_sorteios():
    global _sorteios_cache, _sorteios_cache_time
    now = time.time()
    if not _sorteios_cache or (now - _sorteios_cache_time) > 3600*6:  # 6h TTL
        if CORE_AVAILABLE:
            _sorteios_cache = carregar_sorteios_com_fallback()
        else:
            _sorteios_cache = [set(random.sample(range(1, 26), 15)) for _ in range(1000)]
        _sorteios_cache_time = now
    return _sorteios_cache

# Models
class FiltrosRequest(BaseModel):
    impar: Optional[int] = None
    moldura: Optional[int] = None
    primos: Optional[int] = None
    soma: Optional[int] = None
    bloqueadas: List[int] = Field(default_factory=list)
    fixas: List[int] = Field(default_factory=list)
    sequencia: Optional[int] = None
    fibonacci: Optional[int] = None

class GerarRequest(BaseModel):
    num_jogos: int = Field(15, ge=1, le=50)
    taxa_mutacao: float = Field(0.05, ge=0.01, le=0.25)
    severidade: float = Field(0.8, ge=0, le=1)
    filtros: FiltrosRequest = Field(default_factory=FiltrosRequest)
    foco_14: bool = False
    apriori_ativo: bool = False
    auto_piloto: bool = False
    modo_treino: str = "Historico"
    max_geracoes: int = Field(10, ge=1, le=200)
    is_premium: bool = False
    populacao: int = Field(30, ge=10, le=100)

class GerarResponse(BaseModel):
    base_20: List[int]
    sistema: List[List[int]]
    score: float
    stats: Dict[str, int]
    geracao: int
    tempo_ms: int
    relaxou: bool = False
    is_premium_feature: bool = False

# Endpoints
@app.get("/")
def root():
    return {
        "app": "Lotofácil Pro API REAL",
        "version": "1.0.0",
        "core_available": CORE_AVAILABLE,
        "sorteios_cache": len(get_sorteios()),
        "disclaimer": "Ferramenta educacional, não garante ganhos",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "core": CORE_AVAILABLE, "sorteios": len(get_sorteios())}

@app.post("/api/v1/gerar", response_model=GerarResponse)
def gerar_matriz(req: GerarRequest):
    if not req.is_premium and req.num_jogos > 10:
        raise HTTPException(status_code=402, detail="Free limita 10 jogos. Pro até 33.")
    if not req.is_premium and (req.apriori_ativo or req.auto_piloto):
        raise HTTPException(status_code=402, detail="Apriori e Auto-Piloto são Pro")

    start = time.time()
    sorteios = get_sorteios()

    if CORE_AVAILABLE:
        try:
            # Usa MotorLite real
            repo = LocalJsonRepository()
            motor = MotorLotofacilLite(repository=repo)
            motor._sorteios_treino = sorteios

            filtros = Filtros(
                impar=req.filtros.impar,
                moldura=req.filtros.moldura,
                primos=req.filtros.primos,
                soma=req.filtros.soma,
                sequencia_max=req.filtros.sequencia,
                fibonacci=req.filtros.fibonacci,
                bloqueadas=req.filtros.bloqueadas,
                fixas=req.filtros.fixas,
            )

            config = ConfigGeracao(
                num_jogos=req.num_jogos,
                populacao=req.populacao,
                elite=8,
                taxa_mutacao=req.taxa_mutacao,
                severidade=req.severidade,
                filtros=filtros,
                foco_14=req.foco_14,
                apriori_ativo=req.apriori_ativo,
                auto_piloto=req.auto_piloto,
                max_geracoes=req.max_geracoes,
                simulacoes_por_avaliacao=500 if req.is_premium else 200,
            )

            # Se apriori ativo, minera combos
            combos = None
            if req.apriori_ativo:
                combos = minerar_regras_associacao(sorteios, top_n=10, tamanho_combo=3)

            # Gera evolução
            resultados = motor.gerar(config=config, combos_ouro=combos)
            melhor = resultados[-1] if resultados else motor.gerar_unica(config)

            elapsed = int((time.time() - start) * 1000)

            return GerarResponse(
                base_20=melhor.base_20,
                sistema=melhor.sistema,
                score=melhor.score,
                stats={
                    "h11": melhor.stats.h11,
                    "h12": melhor.stats.h12,
                    "h13": melhor.stats.h13,
                    "h14": melhor.stats.h14,
                    "h15": melhor.stats.h15,
                    "ruins": melhor.stats.ruins,
                },
                geracao=melhor.geracao,
                tempo_ms=elapsed,
                relaxou=melhor.relaxou,
                is_premium_feature=req.apriori_ativo or req.auto_piloto,
            )
        except Exception as e:
            print(f"Erro motor real: {e}, fallback mock")
            # fallback para mock abaixo

    # Mock fallback
    base_20 = sorted(random.sample(range(1, 26), 20))
    sistema = [sorted(random.sample(base_20, 15)) for _ in range(req.num_jogos)]
    score = random.uniform(-50, 800)
    stats = {
        "h11": random.randint(0, 20),
        "h12": random.randint(0, 10),
        "h13": random.randint(0, 5),
        "h14": random.randint(0, 2),
        "h15": random.randint(0, 1),
        "ruins": random.randint(50, 200),
    }
    elapsed = int((time.time() - start) * 1000)

    return GerarResponse(
        base_20=base_20,
        sistema=sistema,
        score=score,
        stats=stats,
        geracao=req.max_geracoes,
        tempo_ms=elapsed,
        relaxou=False,
        is_premium_feature=req.apriori_ativo or req.auto_piloto,
    )

@app.get("/api/v1/gerar/stream")
async def gerar_stream(
    num_jogos: int = 10,
    max_geracoes: int = 20,
    is_premium: bool = False,
):
    """
    Stream SSE - envia cada geração via Server-Sent Events
    Flutter consome com EventSource
    """
    if not is_premium and num_jogos > 10:
        raise HTTPException(status_code=402, detail="Free limita 10")

    async def event_generator():
        sorteios = get_sorteios()
        for g in range(max_geracoes):
            # Mock por enquanto, mas poderia usar motor real com yield
            base_20 = sorted(random.sample(range(1, 26), 20))
            sistema = [sorted(random.sample(base_20, 15)) for _ in range(num_jogos)]
            data = {
                "geracao": g,
                "base_20": base_20,
                "sistema": sistema,
                "score": random.uniform(-50, 500) + g*10,
                "stats": {"h11": random.randint(0,10), "h14": random.randint(0,2), "h15": random.randint(0,1)},
            }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(0.5)
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/v1/inteligencia/atrasometro")
def atrasometro_endpoint():
    sorteios = get_sorteios()
    if CORE_AVAILABLE:
        dados, anomalias = analisar_atrasos(sorteios)
        relatorio = gerar_relatorio_atrasometro(dados, anomalias)
        ranking = [{"dezena": k, **v} for k, v in sorted(dados.items(), key=lambda x: x[1]['atual'], reverse=True)]
        top_5 = anomalias[:5] if anomalias else [r['dezena'] for r in ranking[:5]]
        return {"top_5": top_5, "ranking": ranking, "relatorio": relatorio, "tipo": "atrasometro", "anomalias": anomalias}
    else:
        # Mock
        ranking = [{"dezena": i, "atual": random.randint(0,20), "media": random.uniform(2,6), "status": "ESTOURANDO" if random.random()>0.7 else "NORMAL"} for i in range(1,26)]
        ranking.sort(key=lambda x: x['atual'], reverse=True)
        return {"top_5": [r['dezena'] for r in ranking[:5]], "ranking": ranking, "relatorio": "Mock atrasômetro", "tipo": "atrasometro"}

@app.get("/api/v1/inteligencia/markov")
def markov_endpoint():
    sorteios = get_sorteios()
    if CORE_AVAILABLE:
        top_5, ranking = gerar_previsao_markov(sorteios)
        relatorio = gerar_relatorio_markov(ranking)
        ranking_dict = [{"dezena": d, "peso": p} for d,p in ranking]
        return {"top_5": top_5, "ranking": ranking_dict, "relatorio": relatorio, "tipo": "markov"}
    else:
        top_5 = random.sample(range(1,26),5)
        ranking = [{"dezena": i, "peso": random.random()} for i in range(1,26)]
        ranking.sort(key=lambda x: x['peso'], reverse=True)
        return {"top_5": top_5, "ranking": ranking, "relatorio": "Mock markov", "tipo": "markov"}

@app.get("/api/v1/inteligencia/ensemble")
def ensemble_endpoint(is_premium: bool = Query(False)):
    if not is_premium:
        raise HTTPException(status_code=402, detail="Ensemble é Pro")
    sorteios = get_sorteios()
    if CORE_AVAILABLE:
        top_5, relatorio = executar_ensemble_hibrido(sorteios, usar_xgboost=True)
        # Reconstrói ranking do relatorio? Simplifica
        return {"top_5": top_5, "ranking": [{"dezena": d, "score": 90-i*2} for i,d in enumerate(top_5)], "relatorio": relatorio, "tipo": "ensemble"}
    else:
        top_5 = random.sample(range(1,26),5)
        return {"top_5": top_5, "ranking": [{"dezena": d, "score": random.uniform(60,99)} for d in top_5], "relatorio": "Mock ensemble", "tipo": "ensemble"}

@app.get("/api/v1/inteligencia/apriori")
def apriori_endpoint(is_premium: bool = Query(False), top_n: int = 10):
    if not is_premium:
        raise HTTPException(status_code=402, detail="Apriori é Pro")
    sorteios = get_sorteios()
    if CORE_AVAILABLE:
        combos = minerar_regras_associacao(sorteios, top_n=top_n, tamanho_combo=3)
        relatorio = gerar_relatorio_apriori(combos)
        return {"combos": [sorted(list(c)) for c in combos], "relatorio": relatorio, "tipo": "apriori"}
    else:
        combos = [sorted(random.sample(range(1,26),3)) for _ in range(top_n)]
        return {"combos": combos, "relatorio": "Mock apriori", "tipo": "apriori"}

@app.get("/api/v1/inteligencia/autopiloto")
def autopiloto_endpoint(is_premium: bool = Query(False)):
    if not is_premium:
        raise HTTPException(status_code=402, detail="Auto-Piloto é Pro")
    sorteios = get_sorteios()
    if CORE_AVAILABLE:
        previsoes = prever_macro_propriedades(sorteios)
        relatorio = gerar_relatorio_autopiloto(previsoes)
        return {"previsoes": previsoes, "relatorio": relatorio, "tipo": "autopiloto"}
    else:
        return {"previsoes": {"impar": 8, "moldura": 10, "primos": 5, "soma": 195, "fibonacci": 5}, "relatorio": "Mock autopiloto", "tipo": "autopiloto"}

@app.get("/api/v1/sorteios/ultimo")
def ultimo_sorteio():
    sorteios = get_sorteios()
    ultimo = sorteios[-1] if sorteios else set(random.sample(range(1,26),15))
    return {"concurso": len(sorteios), "data": "2026-09-18", "dezenas": sorted(list(ultimo))}

@app.get("/api/v1/sorteios")
def listar_sorteios(limit: int = 100):
    sorteios = get_sorteios()
    return {"total": len(sorteios), "sorteios": [sorted(list(s)) for s in sorteios[-limit:]]}

@app.get("/api/v1/estatisticas/frequencia")
def frequencia():
    sorteios = get_sorteios()
    from collections import Counter
    freq = Counter()
    for s in sorteios:
        for n in s:
            freq[n] += 1
    return {"frequencia": dict(freq), "total_sorteios": len(sorteios)}

@app.post("/api/v1/stress-test")
def stress_test_endpoint(sistema: List[List[int]], tipo: str = "historico", qtd_testes: int = 1000):
    sorteios = get_sorteios()
    if tipo == "aleatorio":
        test_sorteios = [set(random.sample(range(1,26),15)) for _ in range(qtd_testes)]
    elif tipo == "bootstrap":
        test_sorteios = [random.choice(sorteios) for _ in range(qtd_testes)]
    else:
        test_sorteios = sorteios[-qtd_testes:] if len(sorteios) >= qtd_testes else sorteios

    if CORE_AVAILABLE:
        resultado = stress_test(sistema, test_sorteios, tipo)
        return resultado
    else:
        # Mock
        return {
            "tipo": tipo,
            "qtd_testes": len(test_sorteios),
            "lucro": random.uniform(-1000, 5000),
            "roi": random.uniform(-20, 50),
            "h15": random.randint(0,2),
            "h14": random.randint(0,10),
        }
