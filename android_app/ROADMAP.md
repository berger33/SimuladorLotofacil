# 🗓️ ROADMAP 8 SEMANAS - Lotofácil Pro App

## Semana 1: Fundação e Core Shared

**Objetivo:** Desacoplar core, criar base sólida

- [ ] Dia 1-2: Criar `core_shared/` com domain models, engine lite, ml lite
  - Copiar `fechamento.py`, `filters.py`, `genetic.py` e limpar
  - Criar `repository` pattern para sorteios
  - Remover Queue, customtkinter, multiprocessing obrigatório
  - Testes de paridade: `core` vs `core_shared` devem dar mesmo resultado
- [ ] Dia 3: Refatorar crawler com httpx, TTL, user-agent
- [ ] Dia 4: Criar `api/` FastAPI skeleton com 3 endpoints
- [ ] Dia 5: Setup CI/CD GitHub Actions, pytest, mypy

**Entregável:** `core_shared` testado, API rodando local com /docs

---

## Semana 2: MVP KivyMD

**Objetivo:** APK funcional para beta fechado

- [ ] Dia 1: `kivy_mvp/main.py` com KivyMD, 5 telas bottom navigation
  - Tela Gerador: inputs qtd jogos, fixas, bloqueadas, sliders
  - Tela Dashboard: log + gráfico simples
  - Tela Inteligência: lista atrasômetro/markov
  - Tela Ranking: lista top 50 do JSON local
  - Tela Config: tema
- [ ] Dia 2: Integrar `core_shared` no Kivy, threading para não travar UI
- [ ] Dia 3: Buildozer.spec, testar APK em device físico, ajustar permissões
- [ ] Dia 4: Adicionar AdMob banner (kivy admob lib) + interstitial
- [ ] Dia 5: Beta fechado com 10 amigos, coletar crashes

**Entregável:** APK debug instalável, 5 telas funcionais, geração básica

---

## Semana 3: Flutter Setup + Design System

**Objetivo:** Base Flutter profissional

- [ ] Dia 1: `flutter create flutter_pro`, setup Material 3, google_fonts, flutter_bloc, hive, dio, fl_chart
- [ ] Dia 2: Criar `core/constants`, `core/theme`, `core/utils`, `core/network`, `core/storage`
- [ ] Dia 3: Criar `data` layer: models, datasources, repositories (local + remote)
- [ ] Dia 4: Criar `domain` layer: entities, usecases
- [ ] Dia 5: Criar `presentation/widgets`: heatmap, grafico, card_matriz, slider_custom, empty_state

**Entregável:** Flutter app roda, tema dark/light, widgets base

---

## Semana 4: Flutter Telas Core

**Objetivo:** Telas principais sem backend (mock)

- [ ] Dia 1: Onboarding 3 telas + disclaimer + Hive onboarding_completed
- [ ] Dia 2: Dashboard: gráfico fl_chart, anomalias, atalhos, banner AdMob
- [ ] Dia 3: Gerador: inputs, filtros chips, sliders, bottom sheet logs, BLoC
- [ ] Dia 4: Inteligência: TabBar 4 abas, listas, heatmap, fixar top 5
- [ ] Dia 5: Ranking: lista, detalhes, stress test mock, export/share, favoritar

**Entregável:** 5 telas navegáveis com dados mock, BLoC funcionando

---

## Semana 5: Backend + Integração + Monetização

**Objetivo:** Conectar Flutter com API real e monetizar

- [ ] Dia 1: FastAPI completa: /gerar (stream SSE), /inteligencia/*, /sorteios, deploy Cloud Run
- [ ] Dia 2: Integrar Flutter com API via Dio, cache Hive, offline-first
- [ ] Dia 3: AdMob: banner, interstitial, rewarded + AdsService
- [ ] Dia 4: IAP: produtos no Play Console, in_app_purchase, IAPService, paywall UI
- [ ] Dia 5: Firebase: Analytics, Crashlytics, Remote Config (feature flags), Messaging

**Entregável:** App gera matriz real via API, ads aparecem, paywall mostra

---

## Semana 6: Polimento + Play Store Assets + Beta Fechado

**Objetivo:** Deixar app campeão e preparar Play Store

- [ ] Dia 1: Polimento UI: animações, haptic, shimmer, empty/error states, acessibilidade
- [ ] Dia 2: Criar ícone 512, feature graphic 1024x500, 8 screenshots, vídeo 30s
- [ ] Dia 3: Escrever privacy policy, terms, descrição curta/longa com ASO
- [ ] Dia 4: Checklist Play Store: target SDK 34, data safety, content rating, app bundle assinado
- [ ] Dia 5: Beta fechado: 20 testers, 14 dias obrigatório Google, coletar feedback, corrigir crashes

**Entregável:** AAB pronto, assets prontos, beta fechado rodando

---

## Semana 7: Beta Aberto + Testes

**Objetivo:** Escalar teste e otimizar

- [ ] Dia 1-2: Beta aberto 500 users, monitorar Crashlytics, Analytics funil
- [ ] Dia 3: A/B test paywall preços, otimizar conversão
- [ ] Dia 4: Testes: unit, widget, integration (Patrol), performance em low-end devices
- [ ] Dia 5: Correções finais, changelog, preparar rollout produção

**Entregável:** App estável, métricas boas, pronto produção

---

## Semana 8: Lançamento Produção + Growth

**Objetivo:** Lançar e crescer

- [ ] Dia 1: Produção rollout 20% -> monitorar 24h
- [ ] Dia 2: Rollout 50% -> 100%
- [ ] Dia 3: Post em comunidades (Reddit lotofacil, grupos FB - cuidado com promessa ganhos)
- [ ] Dia 4: Google UAC campanha R$50/dia, ASO experiments
- [ ] Dia 5: Roadmap pós-lançamento: widget Android, notificações, ranking global, iOS

**Entregável:** App em produção, 1k+ instalações, primeiras receitas

---

## Pós-Lançamento (Mês 2-6)

- Mês 2: Feature comunidade, compartilhamento link, notificações sorteios
- Mês 3: Widget Android, Wear OS tile
- Mês 4: iOS com mesmo Flutter
- Mês 5: Web PWA + landing page
- Mês 6: V2 com RL Agent TFLite local, sem backend

## Métricas Sucesso

- Semana 2: APK Kivy instala e gera 1 matriz
- Semana 4: Flutter 5 telas navegáveis
- Semana 5: Geração real via API + paywall
- Semana 6: AAB + beta fechado 20 testers
- Semana 8: Produção com 1k instalações, 3% conversão pro
