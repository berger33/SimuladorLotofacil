"""
FastAPI Backend - Lotofácil Pro
Serve core_shared para Flutter app.

Rodar: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import random
import time
import sys
import os

# Adiciona core_shared
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

app = FastAPI(
    title="Lotofácil Pro API",
    description="API educacional de análise estatística Lotofácil - Não afiliada à Caixa",
    version="1.0.0",
    contact={"name": "Lotofácil Pro", "url": "https://github.com/berger33/SimuladorLotofacil"},
)

# CORS para Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class FiltrosRequest(BaseModel):
    impar: Optional[int] = None
    moldura: Optional[int] = None
    primos: Optional[int] = None
    soma: Optional[int] = None
    bloqueadas: List[int] = Field(default_factory=list)
    fixas: List[int] = Field(default_factory=list)

class GerarRequest(BaseModel):
    num_jogos: int = Field(15, ge=1, le=50, description="Quantidade de jogos")
    taxa_mutacao: float = Field(0.05, ge=0.01, le=0.25)
    severidade: float = Field(0.8, ge=0, le=1)
    filtros: FiltrosRequest = Field(default_factory=FiltrosRequest)
    foco_14: bool = False
    apriori_ativo: bool = False
    auto_piloto: bool = False
    modo_treino: str = "Historico"
    max_geracoes: int = Field(10, ge=1, le=200)
    is_premium: bool = False  # validado via header/token no futuro

class GerarResponse(BaseModel):
    base_20: List[int]
    sistema: List[List[int]]
    score: float
    stats: Dict[str, int]
    geracao: int
    tempo_ms: int
    is_premium_feature: bool = False

class InteligenciaResponse(BaseModel):
    top_5: List[int]
    ranking: List[Dict]
    relatorio: str
    tipo: str

# Mock data - substituir por core_shared real
def mock_sorteios(n=100):
    return [set(random.sample(range(1, 26), 15)) for _ in range(n)]

@app.get("/", tags=["Root"])
def root():
    return {
        "app": "Lotofácil Pro API",
        "version": "1.0.0",
        "disclaimer": "Ferramenta educacional, não garante ganhos, não afiliada à Caixa",
        "docs": "/docs"
    }

@app.get("/api/v1/health", tags=["Health"])
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.post("/api/v1/gerar", response_model=GerarResponse, tags=["Geração"])
def gerar_matriz(req: GerarRequest):
    """
    Gera uma matriz 20 dezenas e desdobramento em N jogos.
    Free limita 10 jogos, premium até 33.
    """
    if not req.is_premium and req.num_jogos > 10:
        raise HTTPException(status_code=402, detail="Free limita 10 jogos. Assine Pro para 33.")

    if req.apriori_ativo and not req.is_premium:
        raise HTTPException(status_code=402, detail="Apriori é feature Pro")

    start = time.time()

    # Mock geração - substituir por core_shared.engine
    base_20 = sorted(random.sample(range(1, 26), 20))
    # Aplica fixas
    if req.filtros.fixas:
        for f in req.filtros.fixas:
            if f not in base_20 and len(base_20) < 20:
                base_20[0] = f
        base_20 = sorted(set(base_20))
        while len(base_20) < 20:
            base_20.append(random.randint(1, 25))
            base_20 = sorted(set(base_20))

    # Desdobramento mock
    sistema = []
    for _ in range(req.num_jogos):
        jogo = sorted(random.sample(base_20, 15))
        # Aplica filtro ímpares mock
        if req.filtros.impar:
            # tenta ajustar
            pass
        sistema.append(jogo)

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
        is_premium_feature=req.apriori_ativo or req.auto_piloto,
    )

@app.get("/api/v1/inteligencia/atrasometro", response_model=InteligenciaResponse, tags=["Inteligência"])
def atrasometro():
    top_5 = random.sample(range(1, 26), 5)
    ranking = [{"dezena": i, "atual": random.randint(0, 20), "media": random.uniform(2, 6), "status": "ESTOURANDO" if random.random()>0.7 else "NORMAL"} for i in range(1, 26)]
    ranking.sort(key=lambda x: x["atual"], reverse=True)
    relatorio = "📊 Atrasômetro - Dezenas com ruptura 2 sigma"
    return InteligenciaResponse(top_5=top_5, ranking=ranking, relatorio=relatorio, tipo="atrasometro")

@app.get("/api/v1/inteligencia/markov", response_model=InteligenciaResponse, tags=["Inteligência"])
def markov():
    top_5 = random.sample(range(1, 26), 5)
    ranking = [{"dezena": i, "peso": random.random()} for i in range(1, 26)]
    ranking.sort(key=lambda x: x["peso"], reverse=True)
    return InteligenciaResponse(top_5=top_5, ranking=ranking, relatorio="🔗 Markov - Probabilidade condicional", tipo="markov")

@app.get("/api/v1/inteligencia/ensemble", response_model=InteligenciaResponse, tags=["Inteligência"])
def ensemble(is_premium: bool = False):
    if not is_premium:
        raise HTTPException(status_code=402, detail="Ensemble é Pro")
    top_5 = random.sample(range(1, 26), 5)
    ranking = [{"dezena": i, "score": random.uniform(60, 99)} for i in range(1, 26)]
    ranking.sort(key=lambda x: x["score"], reverse=True)
    return InteligenciaResponse(top_5=top_5, ranking=ranking, relatorio="👑 Ensemble Híbrido - Conselho Jedi", tipo="ensemble")

@app.get("/api/v1/sorteios/ultimo", tags=["Sorteios"])
def ultimo_sorteio():
    sorteio = sorted(random.sample(range(1, 26), 15))
    return {"concurso": 3500, "data": "2026-09-18", "dezenas": sorteio}

@app.get("/api/v1/sorteios", tags=["Sorteios"])
def listar_sorteios(limit: int = 100):
    sorteios = mock_sorteios(limit)
    return {"total": len(sorteios), "sorteios": [sorted(list(s)) for s in sorteios]}

@app.get("/api/v1/estatisticas/frequencia", tags=["Estatísticas"])
def frequencia():
    freq = {str(i): random.randint(100, 500) for i in range(1, 26)}
    return {"frequencia": freq, "total_sorteios": 3400}
