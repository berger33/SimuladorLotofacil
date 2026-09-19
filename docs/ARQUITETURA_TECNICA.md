# 🏗️ ARQUITETURA TÉCNICA - App Android Lotofácil Pro

## 1. Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLUTTER APP (Android)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Onboard  │ │Dashboard │ │ Gerador  │ │Inteligên.│ │Ranking │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └───┬────┘ │
│       └────────────┴────────────┴────────────┴───────────────┘ │
│                              BLoC / Cubit                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Domain: UseCases (GerarMatriz, AnalisarAtraso, etc)      │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Data: Repositories (Local Hive + Remote Dio)              │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Services: Ads, IAP, Analytics, Crashlytics, Notifications │ │
│  └───────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS / gRPC
┌──────────────────────────▼──────────────────────────────────────┐
│                    FASTAPI BACKEND (Cloud Run)                  │
│  /api/v1/gerar  /api/v1/inteligencia  /api/v1/sorteios         │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ core_shared (Python puro) - genetic_lite, evaluator_lite │ │
│  │ ml_lite (numpy only, xgboost opcional)                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Cache: Redis + SQLite sorteios                            │ │
│  │ Cron: 3x/semana atualiza Caixa                             │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

Alternativa offline-first (sem backend, para KivyMD MVP):
```
KivyMD App
  -> core_shared direto (import)
  -> SQLite local
  -> Crawler direto (requests)
```

## 2. Core Shared - Interface Limpa

### Antes (acoplado):
```python
# engine.py antigo
class MotorLotofacil:
    def __init__(self):
        self.msg_queue = Queue()
        self.params = {} # lê direto da UI
    def loop_genetico(self):
        bloq_str = self.params.get("bloqueadas", "")
        # ...
        self.send_msg("log", status)
```

### Depois (desacoplado):
```python
# core_shared/domain/models.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Filtros:
    impar: Optional[int] = None # None=desativado, int=valor exato
    moldura: Optional[int] = None
    primos: Optional[int] = None
    soma: Optional[int] = None
    sequencia_max: Optional[int] = None
    fibonacci: Optional[int] = None
    bloqueadas: List[int] = None
    fixas: List[int] = None

@dataclass
class ConfigGeracao:
    num_jogos: int = 15
    tam_base: int = 20
    tam_jogo: int = 15
    populacao: int = 50
    elite: int = 10
    taxa_mutacao: float = 0.02
    severidade: float = 0.8
    filtros: Filtros = None
    foco_14: bool = False
    apriori_ativo: bool = False
    auto_piloto: bool = False
    modo_treino: str = "Historico"
    memoria_ativa: bool = True
    hamming: bool = False

@dataclass
class ResultadoGeracao:
    base_20: List[int]
    sistema: List[List[int]]
    score: float
    stats: dict # h11,h12,h13,h14,h15,ruins
    geracao: int
    relaxou: bool
    sharpe: float

# core_shared/engine/engine.py
from typing import Callable, List

class MotorLotofacilLite:
    def __init__(self, 
                 repository: SorteioRepository,
                 on_progress: Callable[[ResultadoGeracao], None] = None,
                 on_anomalia: Callable[[str], None] = None):
        self.repo = repository
        self.on_progress = on_progress
        self.on_anomalia = on_anomalia
        self._rodando = False

    def gerar(self, config: ConfigGeracao) -> List[ResultadoGeracao]:
        # puro, sem Queue, sem UI
        ...

    def parar(self):
        self._rodando = False
```

### Benefícios:
- Testável: `pytest` sem UI
- Reutilizável: Flutter via API chama mesma função, Kivy chama direto
- Tipado: mypy aprova
- Sem dependência de customtkinter, matplotlib, torch

## 3. ML Lite - Sem Torch/XGBoost obrigatório

### Estratégia:
```python
# core_shared/ml/ensemble_lite.py
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

def executar_ensemble_hibrido_lite(sorteios, usar_xgboost=True):
    pontuacao = {i:0.0 for i in range(1,26)}
    
    # 1. Markov (sempre, puro python)
    top_markov, probs_markov = gerar_previsao_markov(sorteios)
    # ... 40%
    
    # 2. Atraso (sempre)
    dados_atraso, anomalias = analisar_atrasos(sorteios)
    # ... 20%
    
    # 3. XGBoost (se disponível e permitido)
    if usar_xgboost and XGBOOST_AVAILABLE:
        # ... 40%
    else:
        # Fallback: usa frequência simples + média móvel
        # 40% distribuído proporcionalmente para markov+atraso
        # ou usa modelo linear numpy
        pass
    
    return top_5, relatorio
```

No mobile:
- Free: `usar_xgboost=False` -> rápido, leve
- Pro: `usar_xgboost=True` se backend, ou False se offline mas com modelo TFLite

### Conversão para TFLite (futuro):
- Treinar XGBoost no backend, exportar para ONNX, converter para TFLite
- Flutter usa `tflite_flutter` para inferência local sem servidor

## 4. Data Layer - Repository Pattern

```python
# core_shared/data/repository.py
from abc import ABC, abstractmethod
from typing import List, Set

class SorteioRepository(ABC):
    @abstractmethod
    def get_todos(self) -> List[Set[int]]:
        pass
    
    @abstractmethod
    def get_recentes(self, n: int) -> List[Set[int]]:
        pass
    
    @abstractmethod
    def salvar_cache(self, sorteios: List[Set[int]]):
        pass

# Implementações:
# - LocalJsonRepository (legado, para desktop)
# - SqliteRepository (mobile offline)
# - RemoteApiRepository (chama Caixa, com fallback)
# - CachedRepository (decorator: tenta remote, se falha usa local, com TTL)
```

Para Flutter, equivalente em Dart:
```dart
abstract class SorteioRepository {
  Future<List<Set<int>>> getTodos();
  Future<List<Set<int>>> getRecentes(int n);
}

class SorteioRepositoryImpl implements SorteioRepository {
  final SorteioLocalDataSource local;
  final SorteioRemoteDataSource remote;
  
  @override
  Future<List<Set<int>>> getTodos() async {
    try {
      final remoteData = await remote.getSorteios();
      await local.cacheSorteios(remoteData);
      return remoteData;
    } catch (e) {
      return await local.getSorteios();
    }
  }
}
```

## 5. Flutter - BLoC Exemplo

```dart
// lib/presentation/blocs/gerador/gerador_bloc.dart
class GeradorBloc extends Bloc<GeradorEvent, GeradorState> {
  final GerarMatrizUseCase gerarMatrizUseCase;
  final AdsService adsService;
  final IAPService iapService;

  GeradorBloc(this.gerarMatrizUseCase, this.adsService, this.iapService) : super(GeradorInitial()) {
    on<GerarMatrizEvent>(_onGerar);
    on<PararGeracaoEvent>(_onParar);
  }

  Future<void> _onGerar(GerarMatrizEvent event, Emitter<GeradorState> emit) async {
    // Checa premium
    final isPremium = await iapService.isPremium();
    if (!isPremium && event.config.numJogos > 10) {
      emit(GeradorPremiumRequired());
      return;
    }

    // Mostra interstitial a cada 3 gerações (free)
    if (!isPremium && await adsService.shouldShowInterstitial()) {
      await adsService.showInterstitial();
    }

    emit(GeradorLoading(geracao: 0));
    
    try {
      await for (final resultado in gerarMatrizUseCase.call(event.config)) {
        emit(GeradorProgress(
          geracao: resultado.geracao,
          score: resultado.score,
          base20: resultado.base_20,
          stats: resultado.stats,
        ));
      }
      emit(GeradorSuccess(...));
    } catch (e) {
      emit(GeradorError(e.toString()));
    }
  }
}
```

## 6. API FastAPI - Contrato

```python
# api/models/request.py
from pydantic import BaseModel, Field
from typing import List, Optional

class FiltrosRequest(BaseModel):
    impar: Optional[int] = Field(None, ge=0, le=15)
    moldura: Optional[int] = None
    primos: Optional[int] = None
    soma: Optional[int] = None
    bloqueadas: List[int] = []
    fixas: List[int] = []

class GerarRequest(BaseModel):
    num_jogos: int = Field(15, ge=1, le=50)
    taxa_mutacao: float = Field(0.02, ge=0.01, le=0.25)
    severidade: float = Field(0.8, ge=0, le=1)
    filtros: FiltrosRequest = FiltrosRequest()
    foco_14: bool = False
    apriori_ativo: bool = False
    auto_piloto: bool = False
    modo_treino: str = "Historico"
    max_geracoes: int = Field(100, ge=1, le=1000)

class GerarResponse(BaseModel):
    base_20: List[int]
    sistema: List[List[int]]
    score: float
    stats: dict
    geracao: int
    tempo_ms: int
```

Endpoints:
- POST /api/v1/gerar -> stream (Server-Sent Events) ou polling
- GET /api/v1/inteligencia/atrasometro
- GET /api/v1/inteligencia/markov
- GET /api/v1/inteligencia/ensemble
- GET /api/v1/sorteios?limit=100
- GET /api/v1/sorteios/ultimo
- GET /api/v1/estatisticas/frequencia

## 7. Segurança e Performance Mobile

- **Sem multiprocessing:** usar `Isolate` no Flutter ou `ThreadPoolExecutor` no Python
- **Bateria:** limitar CPU em background, usar `WorkManager` para geração longa
- **Memória:** populacao 20 no mobile vs 50 desktop, simulações 1000 vs 5000
- **Cache:** Hive para ranking, sorteios, com TTL 6h
- **Ofuscação:** R8 no Android, obfuscate Dart
- **Tamanho APK:** remover torch, tensorflow, usar `numpy` lite, `pandas` opcional

## 8. Estrutura de Pastas Final (Monorepo)

```
SimuladorLotofacil/ (root)
  core/ (legado desktop, mantido)
  core_shared/ (novo, puro, compartilhado)
    domain/
    engine/
    ml/
    data/
    utils/
  ui/ (legado desktop)
  app.py (legado)
  api/ (novo FastAPI)
    main.py
    routers/
    services/
  android_app/
    kivy_mvp/ (MVP rápido)
      main.py
      buildozer.spec
    flutter_pro/ (versão campeã)
      lib/
      android/
      pubspec.yaml
  docs/
    ANALISE_COMPLETA.md
    PLANO_APP_ANDROID.md
    ARQUITETURA_TECNICA.md
    MONETIZACAO_PLAYSTORE.md
    UI_UX_DESIGN_SYSTEM.md
  storage/ (legado, gitignored)
  tests/
  .github/workflows/ci.yml
```

## 9. Migração Gradual (Sem quebrar desktop)

1. Criar `core_shared` copiando `core` e limpando
2. Fazer `core` importar de `core_shared` onde possível (adapter)
3. Desktop continua funcionando, mas usa `core_shared` por baixo
4. Testes garantem paridade: `test_core_shared.py` compara resultados `core` vs `core_shared`
5. Quando 100% paridade, deprecar `core` antigo
