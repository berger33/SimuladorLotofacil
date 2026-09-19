# 📱 Simulador Lotofácil Pro - Branch Aplicativo

> **Branch dedicada à transformação do simulador desktop em App Android comercial campeão de Play Store.**

**Branch:** `Aplicativo` (baseada em `master` f294b19)  
**Status:** Planejamento completo + estrutura base + POCs  
**Preservação:** Todo software desktop original mantido intacto em `core/`, `ui/`, `app.py`

---

## 🎯 Objetivo

Converter o Simulador Lotofácil Pro (CustomTkinter + XGBoost + PyTorch + Algoritmo Genético) em app Android:

- ✅ Mesmas funcionalidades (genético, fechamento, 6 IAs, stress tests, ranking)
- ✅ UI moderna Material 3, amigável, profissional
- ✅ Monetizável: Freemium + AdMob + Subscription
- ✅ Compliance Play Store: privacy, disclaimer jogo responsável, target SDK 34
- ✅ Escalável por anos: arquitetura limpa, core desacoplado, backend opcional

---

## 📚 Documentação Completa (ler nesta ordem)

1. **`docs/ANALISE_COMPLETA.md`** - Auditoria do sistema atual, o que está amador, o que é ouro
2. **`docs/PLANO_APP_ANDROID.md`** - Plano master 8 semanas, 3 opções arquitetura (Kivy vs Flutter vs Nativo), decisão híbrida
3. **`docs/ARQUITETURA_TECNICA.md`** - Diagramas, código desacoplado, repository pattern, BLoC, FastAPI contrato
4. **`docs/MONETIZACAO_PLAYSTORE.md`** - Freemium table, AdMob, IAP, ASO, compliance gambling, assets, checklist lançamento
5. **`docs/UI_UX_DESIGN_SYSTEM.md`** - Cores Material 3, tipografia Outfit/Sora/Inter, componentes, wireframes, animações
6. **`docs/CHECKLIST_PROFISSIONALIZACAO.md`** - Checklist de amador para campeão
7. **`android_app/README.md`** - Como rodar cada versão
8. **`android_app/ROADMAP.md`** - Roadmap dia a dia 8 semanas

---

## 🏗️ Estrutura desta Branch

```
.
├── core/                     # ORIGINAL DESKTOP - mantido intacto
├── ui/                       # ORIGINAL DESKTOP - mantido
├── app.py                    # ORIGINAL
├── config.py                 # ORIGINAL
├── storage/                  # ORIGINAL (gitignored)
│
├── docs/                     # NOVO - Planejamento
│   ├── ANALISE_COMPLETA.md
│   ├── PLANO_APP_ANDROID.md
│   ├── ARQUITETURA_TECNICA.md
│   ├── MONETIZACAO_PLAYSTORE.md
│   ├── UI_UX_DESIGN_SYSTEM.md
│   └── CHECKLIST_PROFISSIONALIZACAO.md
│
├── android_app/              # NOVO - App Android
│   ├── README.md
│   ├── ROADMAP.md
│   ├── core_shared/          # Core puro desacoplado (Python)
│   │   ├── domain/models.py  # Dataclasses, enums, sem UI
│   │   ├── engine/genetic_lite.py
│   │   └── data/repository.py # LocalJson, RemoteApi, Cached
│   ├── kivy_mvp/             # MVP rápido KivyMD + Buildozer
│   │   ├── main.py           # App Kivy 5 telas + motor mock
│   │   └── buildozer.spec    # Gera APK
│   ├── flutter_pro/          # Versão campeã Flutter
│   │   ├── pubspec.yaml
│   │   └── lib/
│   │       ├── main.dart
│   │       └── app.dart      # Material 3 + 5 telas + design system
│   ├── api/                  # FastAPI backend
│   │   └── main.py           # /gerar, /inteligencia, /sorteios
│   ├── playstore/
│   │   ├── privacy_policy.md
│   │   └── listing.md
│   └── monetization/
│       ├── admob_config.md
│       └── iap_config.md
│
└── README_APLICATIVO.md      # Este arquivo
```

---

## 🚀 Como Começar (3 caminhos)

### Caminho 1: Validar rápido com Kivy (1 semana)
```bash
cd android_app/kivy_mvp
pip install kivy kivymd
python main.py  # testa no desktop

# Gerar APK (precisa Linux/WSL)
buildozer android debug
adb install bin/*.apk
```

### Caminho 2: Versão campeã Flutter (recomendado, 6-8 semanas)
```bash
cd android_app/flutter_pro
flutter pub get
flutter run  # precisa Flutter SDK

# Build AAB Play Store
flutter build appbundle --release
```

### Caminho 3: Backend API
```bash
cd android_app/api
pip install fastapi uvicorn
uvicorn main:app --reload --port 8000
# Abrir http://localhost:8000/docs
```

---

## 💡 Decisão Arquitetural Recomendada

**Híbrida em 2 camadas:**
1. **Semana 1-2:** KivyMD MVP para beta fechado rápido, valida mercado, já monetiza com AdMob
2. **Semana 3-8:** Flutter Pro + FastAPI backend para Play Store campeão

**Por que Flutter é campeão:**
- APK 30-50MB vs Kivy 80-150MB
- UI Material 3 nativa 60fps, Play Store ama
- Monetização pronta: google_mobile_ads + in_app_purchase
- Um código gera Android + iOS futuro
- Performance e design 10x superior

**Por que manter core_shared Python:**
- Reaproveita 70% da lógica genética + ML (ouro do sistema)
- Versão Lite sem torch/xgboost para mobile (ou move ML para backend)
- Testável, tipado, sem UI

---

## 💰 Monetização Resumida

| | Free | Pro Anual R$99 |
|---|---|---|
| Jogos | 10 | 33 |
| Gerações | 50 | Ilimitado |
| IA | Atrasômetro, Markov | Todas + Ensemble, Apriori, Auto-Piloto, RL |
| Ads | Banner + Interstitial | Sem ads |
| Export | ❌ | CSV/PDF/WhatsApp |

- **AdMob:** Banner dashboard, interstitial a cada 3 gerações, rewarded para +20 gerações
- **IAP:** Mensal R$19,90, Anual R$99 (58% OFF, 3 dias trial), Vitalício R$199
- **Paywall timing:** Ao tentar >10 jogos, ao clicar feature Pro, após 2 gerações

---

## 📱 Play Store - O que falta para ser comercial

### Críticos já mapeados:
- [ ] Privacy Policy + Data Safety + Content Rating 12+
- [ ] Disclaimer jogo responsável em onboarding + descrição + app
- [ ] Target SDK 34, AAB assinado, 64-bit
- [ ] Categoria Tools, não Gambling, sem promessa "ganhe dinheiro"
- [ ] Ícone 512, feature 1024x500, 5 screenshots, vídeo 30s
- [ ] Teste interno 20 testers 14 dias (obrigatório Google para novos devs)

### Profissionalização:
- [ ] Design system Material 3 com cores roxo/ciano/ouro
- [ ] Onboarding 3 telas + tutorial interativo (não .md)
- [ ] Empty states, shimmer, haptic, animações
- [ ] Firebase Analytics + Crashlytics desde dia 1
- [ ] Offline-first com cache TTL

---

## 🗓️ Roadmap Resumido

- **Semana 1:** core_shared desacoplado + API skeleton
- **Semana 2:** Kivy MVP APK + beta fechado 10 amigos
- **Semana 3:** Flutter setup + design system + widgets base
- **Semana 4:** Flutter 5 telas com mock + BLoC
- **Semana 5:** Backend completo + integração + AdMob + IAP + Firebase
- **Semana 6:** Polimento UI + assets Play Store + beta fechado 20 testers 14 dias
- **Semana 7:** Beta aberto 500 users + A/B paywall + testes performance
- **Semana 8:** Produção 20% -> 100% + growth

Ver `android_app/ROADMAP.md` detalhado dia a dia.

---

## 🔧 Próximos Passos Imediatos

1. **Ler docs na ordem** (2h)
2. **Decidir arquitetura:** Kivy MVP ou Flutter direto? (recomendado: ambos, Kivy para validar, Flutter para campeão)
3. **Criar contas:** Google Play Developer (US$25), AdMob, Firebase
4. **Rodar POCs:** `kivy_mvp/main.py` e `flutter_pro/lib/app.dart`
5. **Começar core_shared:** copiar `core/fechamento.py` e `genetic.py` para `core_shared/` e desacoplar Queue
6. **Setup CI/CD:** GitHub Actions para testes

---

## 📊 Estimativa

- **Esforço:** 30 dias úteis (1 dev senior)
- **Custo infra inicial:** Cloud Run ~US$5/mês + Firebase free tier + Play Console US$25 único
- **Receita potencial:** 10k instalações mês 1 = ~R$10k (R$9.900 assinaturas + R$360 ads), escala para R$100k/mês com 100k instalações

---

## ⚠️ Avisos Legais Importantes

- Este app é **ferramenta educacional de simulação estatística**, não jogo de azar com dinheiro real
- **Não afiliado à Caixa Econômica Federal**
- Loteria é jogo de azar, resultados independentes, **sem garantia de prêmios**
- **Jogue com responsabilidade, +18**
- Se tem problemas com jogo: www.jogoresponsavel.org.br
- Play Store exige disclaimer em 3 lugares + categoria correta + sem promessa ganho

---

## 🤝 Contribuição

Esta branch `Aplicativo` preserva master intacto. Todo novo código Android em `android_app/`, docs em `docs/`. Desktop original continua funcionando com `python app.py`.

Para voltar ao desktop:
```bash
git checkout master
python app.py
```

Para continuar app:
```bash
git checkout Aplicativo
# ver android_app/README.md
```

---

**Desenvolvido com ☕ e IA Avançada - Agora rumo à Play Store! 🚀**
