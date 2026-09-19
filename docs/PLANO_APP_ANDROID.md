# 🚀 PLANO COMPLETO - Transformação Simulador Lotofácil Pro → App Android Comercial

**Objetivo:** Converter o simulador desktop em app Android nativo/híbrido campeão de Play Store, mantendo 100% das funcionalidades, com UI moderna, monetizável e escalável por anos.

**Branch:** `Aplicativo` (preserva master intacto)

---

## FASE 0 - DECISÕES ARQUITETURAIS (Crítico)

### Opção A - Recomendada: Flutter + Python Core via API (Híbrido Profissional)
**Pros:**
- UI 10x mais bonita que Kivy, Material 3 nativo, performance 60fps
- Play Store aprova fácil, APK pequeno (30-50MB)
- Monetização: google_mobile_ads + in_app_purchase já prontos
- Um código Flutter gera Android + iOS futuro
- Python core roda em backend FastAPI (Railway/Fly.io/Cloud Run) ou local via `chaquopy` / `pyo3`
- Time to market: 6-8 semanas

**Contras:** Precisa backend ou bridge

### Opção B - MVP Rápido: KivyMD + Buildozer
**Pros:**
- Reaproveita 90% Python direto, sem backend
- APK em 1 semana
**Contras:**
- UI nunca fica tão profissional quanto Flutter, Play Store pode reclamar de design
- APK grande (80-150MB) com numpy/pandas
- Ads e IAP mais difíceis
- Performance inferior

### Opção C - Nativo Kotlin
**Pros:** Máxima performance, Play Store ama
**Contras:** Reescrever tudo em Kotlin, 3-4 meses, perde todo ML Python

### ✅ DECISÃO FINAL RECOMENDADA: **Arquitetura Híbrida em 2 Camadas**
```
Camada 1 - MVP (Semana 1-2): KivyMD + Buildozer para validar mercado rápido
Camada 2 - PRO (Semana 3-8): Flutter + FastAPI backend + Core Python Lite
```
Assim você lança rápido e já monetiza, enquanto constrói versão campeã.

---

## FASE 1 - REFATORAÇÃO DO CORE (Semana 1)

### 1.1 Criar `core_shared/` desacoplado
```
core_shared/
  __init__.py
  domain/
    models.py - dataclasses: Jogo, Matriz, Sorteio, Estatisticas, Configuracao
    enums.py - ModoTreino, TipoFiltro, Estrategia
  engine/
    genetic_lite.py - sem customtkinter, sem queue, puro python
    evaluator_lite.py - sem multiprocessing, retorna objeto
    fechamento.py - manter igual, já puro
    filters.py - manter
  ml/
    atrasometro.py - puro python + numpy
    markov.py - puro
    ensemble_lite.py - XGBoost opcional, fallback para média móvel se não disponível
    apriori.py
    autopiloto.py
  data/
    repository.py - interface abstrata
    local_repository.py - SQLite/Room
    remote_repository.py - API Caixa + cache TTL
    crawler.py - refatorado com httpx, retry, user-agent
  utils/
    logger.py - abstração para Crashlytics no mobile
    math_utils.py - sharpe, hamming
```

**Mudanças obrigatórias no core atual:**
- Remover `from ui.interface import` de todo core (não tem, ok)
- Remover `queue` e `send_msg` do engine, trocar por callbacks / observer pattern
- Trocar `load("melhores_matriz_*.json")` por injeção de dependência repository
- Trocar `ProcessPoolExecutor` por `concurrent.futures.ThreadPoolExecutor` + opção `use_multiprocess=False` para mobile
- Remover `torch` obrigatório, tornar opcional: `try: import torch except: TORCH_AVAILABLE=False` já existe, mas precisa garantir que engine funciona sem torch
- Criar `core_shared/config.py` com Pydantic Settings, não constantes soltas
- 100% tipado com `typing` + docstrings

### 1.2 Criar API FastAPI (para Flutter)
```
api/
  main.py - FastAPI app
  routers/
    geracao.py - POST /gerar - recebe filtros, retorna matriz
    inteligencia.py - GET /atrasometro, /markov, /ensemble
    historico.py - GET /sorteios, /estatisticas
    ranking.py - GET /ranking, POST /salvar
  services/
    engine_service.py - orquestra core_shared
  models/
    request.py - Pydantic
    response.py
```

---

## FASE 2 - APP ANDROID - ESTRUTURA FLUTTER (Semana 2-4)

### 2.1 Estrutura de pastas Flutter (Recomendada)
```
android_app/flutter_lotofacil/
  lib/
    main.dart
    app.dart
    core/
      constants/ - colors.dart, strings.dart, config.dart
      theme/ - app_theme.dart (Material 3, light/dark)
      utils/ - helpers, validators, formatters
      network/ - dio client, interceptors, cache
      storage/ - hive / isar local DB
    data/
      datasources/ - local (Hive), remote (API)
      models/ - jogo_model.dart (fromJson)
      repositories/ - implementações
    domain/
      entities/ - jogo.dart, matriz.dart
      repositories/ - interfaces
      usecases/ - gerar_matriz, analisar_atrasos, etc
    presentation/
      screens/
        onboarding/ - 3 telas: bem-vindo, como funciona, disclaimer
        dashboard/ - overview lucro, últimos sorteios, atalhos
        gerador/ - controles: qtd jogos, filtros, fixas/bloqueadas, sliders mutação/severidade
        inteligencia/ - abas: Atrasômetro, Markov, Ensemble, Apriori, Auto-Piloto
        ranking/ - top 50, top 3, detalhes, stress test, export/share
        configuracoes/ - tema, banca, idioma, premium, privacy
        premium/ - paywall, benefícios, comparação free vs pro
      widgets/
        heatmap_widget.dart - 5x5 grid animado
        grafico_convergencia.dart - fl_chart
        card_matriz.dart
        slider_custom.dart
        filtro_chip.dart
      blocs/ - flutter_bloc para cada feature (gerador_bloc, inteligencia_bloc, ranking_bloc)
    services/
      ads_service.dart - AdMob banner, interstitial, rewarded
      iap_service.dart - in_app_purchase
      analytics_service.dart - Firebase Analytics
      crashlytics_service.dart
      notification_service.dart - FCM
  android/ - gradle, manifest com permissions
  assets/
    images/ - logo, onboarding illustrations
    lottie/ - animações
  pubspec.yaml
```

### 2.2 Features por tela (Todas as funcionalidades atuais mapeadas)

**Onboarding (Novo - Essencial Play Store):**
- Tela 1: Logo + "Laboratório de IA para Lotofácil" + Lottie foguete
- Tela 2: "Como funciona" com 3 cards: Genético, Inteligência, Fechamento
- Tela 3: Disclaimer legal obrigatório: "Ferramenta estatística, não garante ganhos, +18, jogo responsável" + checkbox aceito + botão Começar
- Salva `onboarding_completed` no Hive

**Dashboard (Equivalente ao log + anomalias + gráfico):**
- Header: Saldo top 1, média população, drawdown
- Card: Último sorteio Caixa (API)
- Gráfico convergência (fl_chart) - Top vs Média
- Lista anomalias (últimas 5)
- Atalhos: Gerar nova matriz, Ver ranking, Rodar IA
- Banner AdMob (free)

**Gerador (Painel de Controle antigo):**
- Top: Seletor Qtd Jogos (10 free, 15, 20, 33 premium) - se free tentar 33, mostra paywall
- Seção DNA: Fixas (chips), Bloqueadas (chips), Qtd Jogos
- Seção Filtros: Chips expansíveis: Ímpares, Moldura, Primos, Soma, Sequência, Fibonacci + Auto-Piloto toggle (premium)
- Seção Hiperparâmetros: Sliders Mutação e Severidade + switches: Memória, Hamming, Foco 14 (Cofre Seguro)
- Seção Estratégia: Cards: Conservador, Agressivo, Robô Preguiçoso (combina Apriori+Auto+RL)
- Botão grande: "▶️ Iniciar Motor Híbrido" -> mostra bottom sheet com logs ao vivo + botão Pausar/Parar/Turbo
- Durante geração: mostra progresso, geração atual, lucro estimado

**Inteligência (Atrasômetro / IA antigo):**
- TabBar: Atrasômetro, Markov, Ensemble, Apriori
- Cada aba: lista com scores, botão "Fixar Top 5"
- Card explicação: o que é cada IA
- Botão: Rodar todas (para premium roda ensemble completo, free só atrasômetro+markov)
- Heatmap 5x5 interativo, cores Material

**Ranking (Top 50 + Top 3 + Detalhes):**
- Segmented control: Top 50, Top 3, Meus Favoritos
- Lista: Card por matriz: posição, saldo, base 20, stats 11-15
- Ao clicar: Detalhes da Matriz - base 20 grande, lista jogos com copy/share, botão Stress Test (3 opções), botão Exportar CSV/PDF, botão Favoritar, botão Compartilhar WhatsApp
- Swipe para deletar (com confirmação)
- Botão snapshot

**Premium / Monetização:**
- Tela paywall: Comparativo Free vs Pro
- Free: 10 jogos, 50 gerações, ads, sem Ensemble, sem Auto-Piloto, sem RL, sem export
- Pro (R$19,90/mês ou R$99/ano ou R$199 vitalício): tudo ilimitado, sem ads, IA completa, 33 jogos, turbo, notificações, suporte
- Botões: Assinar mensal, anual (com desconto), vitalício, Restaurar compras
- Se já premium, mostra "Você é Pro" + benefícios

**Configurações:**
- Tema: Claro, Escuro, Sistema
- Idioma: PT-BR, EN-US
- Banca: valor para gestão risco
- Notificações: toggle
- Links: Privacy Policy, Terms, Tutorial, Avaliar app, Contato
- Versão

### 2.3 Design System - Para ser campeão

**Cores (Material 3):**
- Primary: #6F42C1 (roxo IA)
- Secondary: #17A2B8 (ciano Markov)
- Tertiary: #FFD700 (ouro Apriori)
- Error: #DC3545
- Success: #28A745
- Background dark: #121212, light: #FAFAFA
- Surface: cards com elevação

**Tipografia:**
- Display: Outfit Bold 32
- Headline: Sora SemiBold 24
- Body: Inter Regular 16
- Mono para números: JetBrains Mono

**Componentes:**
- Cards com border radius 16, elevação 2
- Botões filled, tonal, outlined
- Chips para dezenas
- Sliders com valor
- Bottom sheets
- Shimmer loading
- Empty states com ilustração
- Lottie para sucesso (jackpot)

**Animações:**
- Hero animation ao abrir detalhes
- AnimatedContainer no heatmap
- Fade + slide nas listas
- Confetti quando 15 pontos em stress test

---

## FASE 3 - MONETIZAÇÃO E PLAY STORE (Semana 4-5)

### 3.1 Monetização (Ver doc separado)
- AdMob: banner no dashboard, interstitial a cada 3 gerações, rewarded para liberar 1 geração extra
- IAP: subscription mensal/anual/vitalício via Google Play Billing Library 6
- Freemium com feature gating
- Afiliados: link para loterias online (se permitido)

### 3.2 Compliance Play Store (Checklist)
- [ ] Target SDK 34, compile SDK 34
- [ ] 64-bit (Flutter já é)
- [ ] Privacy Policy URL (hospedar no GitHub Pages / Notion)
- [ ] Data Safety form: coleta? Sim - analytics anonimizado, crash logs, não coleta dados pessoais sensíveis
- [ ] Disclaimer: "Este app é ferramenta educacional de análise estatística, não é jogo de azar, não garante prêmios, não afiliado à Caixa, +18"
- [ ] Classificação: Everyone? Mas com aviso de simulação de jogo -> PEGI 12 ou Teen
- [ ] Ícone 512x512, feature graphic 1024x500, screenshots 5x phone + 1x tablet
- [ ] Short description 80 chars, full description 4000 chars com keywords: lotofácil, análise, estatística, inteligência artificial, desdobramento
- [ ] App Bundle (AAB) assinado
- [ ] Teste interno, fechado, aberto antes de produção
- [ ] Sem permissão desnecessária (só INTERNET, BILLING)
- [ ] Sem promessa de ganho financeiro

---

## FASE 4 - BACKEND E INFRA (Semana 3)

- FastAPI hospedado em Cloud Run (escala a zero, barato)
- Redis para cache sorteios (TTL 6h)
- Cron job 3x por semana puxa resultados Caixa (após sorteios seg  qua sex)
- Firebase: Auth anônimo, Firestore para ranking global opcional, Analytics, Crashlytics, Remote Config, Messaging
- Sentry para logs backend

---

## FASE 5 - DEVOPS E QUALIDADE

- GitHub Actions: lint, test, build APK/AAB
- Fastlane para deploy Play Store
- Testes: unit (core_shared), widget (Flutter), integration (Patrol)
- Versionamento: semver 1.0.0 -> 1.1.0
- Changelog
- Code push via Shorebird (para Flutter) - atualiza sem passar pela Play Store

---

## FASE 6 - LANÇAMENTO E CRESCIMENTO

**Semana 6: Beta fechado**
- 20 testers, coleta feedback, ajusta paywall

**Semana 7: Beta aberto**
- 500 users, AdMob teste, IAP teste

**Semana 8: Produção**
- Lançamento com ASO, screenshots profissionais, vídeo preview
- Post em comunidades lotofácil (cuidado para não prometer ganhos)
- Anúncios Google UAC

**Pós-lançamento:**
- Semana 9-12: Feature: Comunidade (ranking global), Compartilhar jogos com link, Notificação de novos sorteios, Widget Android
- Mês 4: iOS (mesmo Flutter)
- Mês 6: Versão Web PWA

---

## ESTIMATIVA DE ESFORÇO

- Refator core_shared: 3 dias
- API FastAPI: 2 dias
- Flutter app (MVP): 15 dias
- KivyMD MVP (paralelo): 5 dias
- Play Store assets + compliance: 2 dias
- Monetização: 3 dias
- Testes + CI/CD: 3 dias
- Total: ~30 dias úteis (1 dev senior)

---

## RISCOS E MITIGAÇÕES

- **APK grande com ML:** Mitigar com ensemble_lite sem xgboost/torch, ou backend
- **Play Store rejeita por gambling:** Mitigar com disclaimer forte, classificar como Education/Tools, não usar palavras "aposte", "ganhe dinheiro", usar "simulação estatística"
- **Crawler Caixa bloqueia:** Mitigar com cache, múltiplos endpoints, user-agent rotativo, backend com proxy
- **Performance em device fraco:** Mitigar com limite gerações free, modo lite, turbo desabilitado em low-end

---

## ENTREGÁVEIS DESTA BRANCH

- [x] Análise completa
- [x] Plano de implementação (este doc)
- [ ] Arquitetura técnica detalhada
- [ ] Design system
- [ ] Monetização doc
- [ ] Estrutura android_app/ com exemplos
- [ ] POC KivyMD main.py
- [ ] POC Flutter lib/main.dart
- [ ] FastAPI skeleton
- [ ] Buildozer.spec
- [ ] Play Store checklist + privacy policy template
