# Core Shared - Biblioteca Pura

Biblioteca desacoplada que pode ser usada por:
- Desktop (CustomTkinter)
- Kivy Android
- Flutter via API
- FastAPI backend
- Testes

## Estrutura
```
core_shared/
  domain/
    models.py - ConfigGeracao, ResultadoGeracao, Matriz, etc
    enums.py - ModoTreino, TierUsuario, etc
  engine/
    genetic_lite.py - gerar_sistema, crossover, mutacao
    fechamento.py - desdobramento 20->15 com relaxamento
    evaluator_lite.py - avalia com Sharpe + bonus Apriori
    engine.py - MotorLotofacilLite com callbacks (sem Queue)
  ml/
    atrasometro.py - desvio padrão ruptura 2 sigma
    markov.py - matriz transição 25x25
    ensemble_lite.py - 40% Markov + 20% Atraso + 40% XGBoost ou fallback frequência
    apriori.py - mineração trincas
    autopiloto.py - prevê soma, ímpares, etc
  data/
    repository.py - SorteioRepository, LocalJson, RemoteApi, Cached
    crawler.py - 3 endpoints Caixa + cache
  utils/
    math_utils.py - sharpe, hamming, etc
    logger.py - abstraído para Crashlytics
  config.py - Pydantic Settings ou fallback
  tests/
    test_core_shared.py - 9 testes passando
```

## Uso
```python
from core_shared.data.crawler import carregar_sorteios_com_fallback
from core_shared.data.repository import LocalJsonRepository
from core_shared.engine.engine import MotorLotofacilLite
from core_shared.domain.models import ConfigGeracao, Filtros

sorteios = carregar_sorteios_com_fallback()
repo = LocalJsonRepository()
motor = MotorLotofacilLite(repository=repo, on_progress=lambda r: print(f"G{r.geracao} Score {r.score}"))
motor._sorteios_treino = sorteios

config = ConfigGeracao(
    num_jogos=10,
    populacao=20,
    max_geracoes=50,
    filtros=Filtros(impar=8, bloqueadas=[25]),
    foco_14=False,
)

resultados = motor.gerar(config=config)
melhor = resultados[-1]
print(f"Top: {melhor.base_20} Score {melhor.score}")
```

## Testes
```bash
pytest android_app/core_shared/tests/test_core_shared.py -v
# 9 passed
```

## Diferença vs core/ original
- Sem customtkinter, sem Queue, sem multiprocessing obrigatório
- Injeção de dependência repository
- Tipado, testável
- Funciona sem torch/xgboost (fallback)
- Callbacks ao invés de msg_queue
- Mesmo algoritmo genético + fechamento com relaxamento
