# API - Lotofácil Pro

FastAPI backend que serve core_shared para Flutter.

## Endpoints

- `GET /` - info
- `GET /api/v1/health` - health check
- `POST /api/v1/gerar` - gera matriz (com validação freemium)
- `GET /api/v1/gerar/stream` - SSE stream por geração
- `GET /api/v1/inteligencia/atrasometro` - dados atrasômetro
- `GET /api/v1/inteligencia/markov` - markov
- `GET /api/v1/inteligencia/ensemble?is_premium=true` - ensemble (Pro)
- `GET /api/v1/inteligencia/apriori?is_premium=true` - combos ouro
- `GET /api/v1/inteligencia/autopiloto?is_premium=true` - prevê filtros
- `GET /api/v1/sorteios/ultimo` - último sorteio
- `GET /api/v1/sorteios?limit=100` - lista
- `GET /api/v1/estatisticas/frequencia` - frequência
- `POST /api/v1/stress-test` - stress test

## Rodar local

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# ou com core real
uvicorn main_real:app --reload --port 8000
```

Docs: http://localhost:8000/docs

## Deploy Cloud Run

```bash
gcloud run deploy lotofacil-api --source . --region us-central1 --allow-unauthenticated --set-env-vars API_ENV=prod
```

## Diferença main.py vs main_real.py

- `main.py` - mock rápido, sem dependência core_shared, bom para testar Flutter sem backend completo
- `main_real.py` - usa core_shared de verdade, precisa sorteios cache, mais pesado mas real

## Freemium

- Free limita 10 jogos, sem apriori/autopiloto/ensemble
- Pro via `is_premium=true` (em produção validar token JWT ou purchase token)
