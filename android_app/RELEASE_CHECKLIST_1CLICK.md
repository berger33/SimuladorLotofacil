# ✅ RELEASE CHECKLIST 1-CLIQUE - Lotofácil Pro Play Store

**Use este checklist para lançar em produção sem esquecer nada. Marque cada item.**

---

## Pré-Requisitos (Uma vez)

- [ ] Conta Google Play Developer paga US$25 e verificada (RG)
- [ ] Flutter SDK instalado (3.16+)
- [ ] Android Studio + SDK 34
- [ ] Keystore gerado: `keytool -genkey -v -keystore ~/lotofacil-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload`
- [ ] `android_app/flutter_pro/android/key.properties` preenchido com senhas (NÃO commitar)
- [ ] Service Account Play Console JSON `play-console-service-account.json` (para Fastlane)
- [ ] Contas: AdMob, Firebase, GitHub

---

## Assets (Dia 1) - ✅ JÁ GERADOS COM IA

- [x] Ícone 512x512 `icon.png` 1.9MB - GERADO IA
- [x] Adaptive foreground `icon_foreground.png` 432x432 - GERADO
- [x] Adaptive background `icon_background.png` 432x432 - GERADO
- [x] Feature Graphic 1024x500 `feature_graphic.png` 2.4MB - GERADO
- [x] 9 Screenshots 1080x1920 (01_dashboard até 09_config) - GERADOS
- [ ] Splash clean `splash_clean.png` 1080x1920 - GERADO (copiado do ícone, pode melhorar)
- [ ] Vídeo preview 30s `video_preview_30s.mp4` - STORYBOARD PRONTO, script `create_video.sh` pronto, precisa gravar screen recording
- [ ] Otimizar imagens: `./scripts/optimize_images.sh` (precisa TINYPNG_API_KEY ou pngquant)

**Comando otimizar:**
```bash
cd android_app
export TINYPNG_API_KEY=sua_key_tinypng # opcional, melhor qualidade
./scripts/optimize_images.sh
```

---

## Build AAB (Dia 2)

- [ ] `cd android_app/flutter_pro && flutter pub get`
- [ ] `flutter analyze` - 0 erros
- [ ] `flutter test` - se tiver testes
- [ ] Gerar AAB release:
```bash
./scripts/build_aab.sh
# ou
cd flutter_pro && flutter build appbundle --release
# Saída: build/app/outputs/bundle/release/app-release.aab ~20MB
```
- [ ] Verificar tamanho <150MB (Flutter ~20MB OK)
- [ ] Verificar `targetSdk 34` em `android/app/build.gradle`
- [ ] Testar AAB em device: `bundletool build-apks --bundle=app-release.aab --output=app.apks && bundletool install-apks --apks=app.apks`

---

## GitHub Pages Privacy (Dia 2)

- [ ] GitHub repo > Settings > Pages > Source: Deploy from branch > Branch: Aplicativo / docs folder > Save
- [ ] Aguardar 2 minutos deploy
- [ ] Testar URLs:
  - https://berger33.github.io/SimuladorLotofacil/ (landing)
  - https://berger33.github.io/SimuladorLotofacil/privacy.html (privacy policy)
  - https://berger33.github.io/SimuladorLotofacil/terms.html (terms)
- [ ] Copiar privacy URL para Play Console

---

## Play Console - Criar App (Dia 3)

### Criação
- [ ] Play Console > Criar app
  - Nome: Lotofácil Pro - IA & Estatística
  - Idioma: pt-BR
  - App ou jogo: App
  - Gratuito
  - Declarações: NÃO é jogo com dinheiro real, é ferramenta educacional

### Configuração Obrigatória
- [ ] **Painel > Configurar app:**
  - [ ] Categoria: Ferramentas
  - [ ] Tags: lotofácil, análise, estatística, desdobramento, IA
  - [ ] Email contato: suporte@lotofacilpro.com
  - [ ] Privacy Policy URL: https://berger33.github.io/SimuladorLotofacil/privacy.html
  - [ ] É app de notícias? Não
  - [ ] É app COVID? Não

- [ ] **Política > Conteúdo do app:**
  - [ ] Questionário conteúdo: Simula jogo azar sem dinheiro real? Sim → 12+ Teen
  - [ ] Público-alvo: 18+
  - [ ] Anúncios: Sim, AdMob
  - [ ] Data Safety: Preencher (ver `playstore/listing.md`)
    - Coleta: ID dispositivo, analytics, crash
    - Compartilha: Google
    - Criptografia: Sim
    - Deletar: Sim
  - [ ] Criptografia: NÃO usa criptografia não padrão

- [ ] **Monetização > Produtos:**
  - [ ] Criar assinatura mensal `lotofacil_pro_monthly` R$19,90
  - [ ] Criar anual `lotofacil_pro_yearly` R$99,90 com 3 dias trial
  - [ ] Criar produto único `lotofacil_pro_lifetime` R$199,90

- [ ] **Crescimento > Recursos gráficos:**
  - [ ] Ícone 512x512
  - [ ] Feature Graphic 1024x500
  - [ ] 9 Screenshots 1080x1920
  - [ ] Vídeo preview YouTube não listado (opcional mas recomendado)

- [ ] **Qualidade > Teste interno:**
  - [ ] Criar lista testers: 20 emails (amigos, família)
  - [ ] Adicionar lista ao teste interno
  - [ ] Copiar link teste interno e enviar para 20 pessoas
  - [ ] Instruir: instalar, gerar matriz, usar 5 min/dia por 14 dias

### Upload AAB Teste Interno
- [ ] Teste interno > Criar nova versão > Upload `app-release.aab`
- [ ] Notas: "Primeira versão com IA completa, 3675 sorteios, motor genético, 5 telas Material 3"
- [ ] Salvar > Revisar > Iniciar lançamento teste interno
- [ ] Aguardar Google revisar (2-12h)

---

## Teste Interno 14 Dias Obrigatório (Dia 3-17)

**Google exige para novos devs:** 20 testers, 14 dias contínuos, app instalado e usado.

- [ ] Enviar link para 20 testers
- [ ] Acompanhar Play Console > Teste interno > Testers: 20 ativos?
- [ ] Pedir feedback diário nos primeiros 3 dias
- [ ] Monitorar Crashlytics (se Firebase configurado)
- [ ] NÃO subir nova AAB nos 14 dias a menos que crash crítico (reinicia contador)

**Enquanto teste roda, fazer em paralelo:**

#### Backend (Dia 4-5)
- [ ] `cd android_app/api && gcloud run deploy lotofacil-api --source . --region us-central1 --allow-unauthenticated`
- [ ] Testar https://lotofacil-api-xxx.run.app/docs
- [ ] Atualizar Flutter `dio_client.dart` baseUrl para Cloud Run URL

#### Firebase (Dia 6)
- [ ] Firebase Console > Criar projeto lotofacil-pro
- [ ] Adicionar Android app package com.berger33.lotofacilpro
- [ ] Baixar google-services.json para `android/app/`
- [ ] Ativar Analytics, Crashlytics, Remote Config, Messaging
- [ ] AdMob: criar App ID produção, trocar teste IDs em `ads_service.dart` e `AndroidManifest.xml`

#### Monetização UI (Dia 7-8)
- [ ] Integrar `BannerAdWidget` real no dashboard e ranking
- [ ] Interstitial a cada 3 gerações (já tem `shouldShowInterstitial`)
- [ ] Rewarded +20 gerações
- [ ] Paywall com `IAPService` real buyMonthly/yearly/lifetime + restore

#### Polimento (Dia 9-10)
- [ ] Testes em 5 devices físicos low-end a high-end
- [ ] Cold start <2s, geração 10 jogos <5s
- [ ] Acessibilidade TalkBack, contraste AA, 48dp
- [ ] Haptic, animações 60fps, shimmer, empty/error states

---

## Beta Fechado/Aberto (Dia 17)

- [ ] Após 14 dias OK, promover: Teste interno → Fechado (100 testers) → Aberto (500 testers)
- [ ] Monitorar reviews, crashes, ANRs
- [ ] Responder reviews <24h

---

## Produção Rollout Gradual (Dia 18+)

- [ ] Produção > Criar nova versão > Upload mesma AAB (ou nova com fixes)
- [ ] Rollout 20% > monitorar 24h Crashlytics/Analytics
- [ ] Rollout 50% > 24h
- [ ] Rollout 100%

---

## Pós-Lançamento Crescimento

- [ ] Responder reviews <24h nos primeiros 30 dias (crítico ranking)
- [ ] ASO Experiments: testar ícone, screenshots, descrição curta
- [ ] Google UAC campanha R$50/dia
- [ ] Blog SEO + Telegram/Discord Pro
- [ ] Roadmap: widget Android, notificações sorteios, ranking global, iOS

---

## Comandos 1-Clique

```bash
# Tudo em um (após configurar keystore e key.properties)
cd android_app
./scripts/optimize_images.sh          # otimiza imagens
cd flutter_pro && flutter build appbundle --release  # AAB
# ou
./scripts/build_aab.sh                # script completo

# Fastlane (precisa service account JSON)
cd flutter_pro/android
fastlane internal                     # build + upload teste interno
fastlane production_20                # 20% produção após 14 dias

# Vídeo
cd ../playstore/video_preview
./create_video.sh                     # screenshots -> video 30s

# GitHub Pages já ativo se branch Aplicativo / docs
# URL: https://berger33.github.io/SimuladorLotofacil/privacy.html
```

---

## Checklist Final Antes de Produção 100%

- [ ] AAB assinado, targetSdk 34, minSdk 24, 64-bit, <150MB
- [ ] Ícone 512, feature 1024x500, 5+ screenshots 1080x1920, vídeo 30s
- [ ] Descrição curta 80 chars, longa 4000 com keywords, disclaimer legal 3 lugares
- [ ] Privacy Policy URL pública funcionando
- [ ] Data Safety preenchido
- [ ] Content rating 12+ Teen
- [ ] Categoria Tools, não Gambling
- [ ] Sem permissão desnecessária (só INTERNET, BILLING, POST_NOTIFICATIONS)
- [ ] Sem promessa "ganhe dinheiro", só "análise estatística"
- [ ] Teste interno 20 testers 14 dias completo OK
- [ ] Produtos IAP criados e ativos
- [ ] AdMob IDs produção (não teste)
- [ ] Firebase Crashlytics 0 crashes
- [ ] Cold start <2s, geração <5s mid-end
- [ ] AAB testado em 5 devices físicos

---

**Tempo total estimado:** 18 dias (2 dias assets/build + 14 dias teste obrigatório Google + 2 dias rollout)
**Custo:** US$25 Play Console + ~US$5/mês Cloud Run + Firebase free tier
**Receita potencial Mês 1:** 10k instalações, 5% conversão Pro anual R$99 = R$9.900 + ads R$360 = ~R$10k
