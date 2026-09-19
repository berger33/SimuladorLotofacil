# 🚀 PRÓXIMOS PASSOS - Publicar na Play Store (Guia Prático)

**Status atual:** 80% completo, Flutter produção 95%, core 100%, AAB pronto para gerar
**Tempo até produção:** 16 dias (2 dias assets + 14 dias teste obrigatório Google)

---

## Dia 1: Assets Visuais (HOJE)

### 1.1 Ícone 512x512
- [ ] Criar no Figma ou https://icon.kitchen/
- Fundo gradiente roxo #6F42C1 -> #4A1A8B
- Símbolo: L + gráfico + estrela, sem texto
- Exportar `icon.png` 512x512 PNG 32-bit
- Colocar em `android_app/flutter_pro/assets/images/icon.png`
- Rodar: `flutter pub run flutter_launcher_icons`

### 1.2 Feature Graphic 1024x500
- [ ] Figma 1024x500, sem transparência
- Título: "Lotofácil Pro - IA & Estatística"
- Sub: "Desdobramentos Inteligentes"
- Visual: mockup celular com heatmap + gráfico + bolas lotofácil
- Exportar `feature_graphic.png`
- Salvar em `android_app/playstore/assets/`

### 1.3 Screenshots (1080x1920)
- [ ] Rodar app Flutter: `flutter run` e tirar screenshots de:
  1. dashboard - gráfico + top score
  2. gerador - filtros + sliders
  3. inteligencia - heatmap + Top 5
  4. ranking - lista cards
  5. detalhes - base 20 + jogos
  6. premium - paywall
  7. onboarding - bem-vindo
- [ ] Usar device frame: https://www.previewed.app/ ou Figma
- [ ] Salvar em `android_app/playstore/assets/screenshots/`

### 1.4 Vídeo Preview (opcional mas recomendado)
- [ ] Screen recording 30s com narração
- [ ] Upload YouTube não listado
- [ ] Link no Play Console

---

## Dia 2: Build AAB Assinado + Privacy

### 2.1 Keystore (uma vez)
```bash
keytool -genkey -v -keystore ~/lotofacil-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
# Senha: escolher forte, guardar em .env e 1Password
```

### 2.2 android/key.properties
```bash
cat > android_app/flutter_pro/android/key.properties <<EOF
storePassword=SUA_SENHA_FORTE
keyPassword=SUA_SENHA_FORTE
keyAlias=upload
storeFile=/home/user/lotofacil-upload-keystore.jks
EOF
# Adicionar ao .gitignore (já está)
```

### 2.3 Build AAB
```bash
cd android_app/flutter_pro
flutter build appbundle --release
# Saída: build/app/outputs/bundle/release/app-release.aab
# Tamanho esperado: ~20MB
```

### 2.4 Privacy Policy Hospedada
- [ ] Criar GitHub Pages: Settings > Pages > Source: main / docs
- [ ] Ou criar `docs/privacy.html` com conteúdo de `android_app/playstore/privacy_policy.md`
- [ ] URL: `https://berger33.github.io/SimuladorLotofacil/privacy`
- [ ] Testar URL pública
- [ ] Adicionar em Play Console > Política de privacidade

---

## Dia 3: Play Console - Criar App

### 3.1 Conta
- [ ] https://play.google.com/console - pagar US$25
- [ ] Verificar identidade (RG, comprovante)

### 3.2 Criar App
- Nome: Lotofácil Pro - IA & Estatística
- Idioma padrão: pt-BR
- App ou jogo: App
- Gratuito ou pago: Gratuito (com compras no app)
- Declarações: jogo com dinheiro? NÃO, é ferramenta educacional

### 3.3 Configurar
- [ ] Categoria: Ferramentas
- [ ] Tags: lotofácil, análise, estatística, desdobramento, IA
- [ ] Contato: email suporte
- [ ] Privacy Policy URL
- [ ] Data Safety: preencher (coleta ID dispositivo, analytics, crash, compartilha com Google, criptografia sim, deletar sim)
- [ ] Content Rating: IARC questionário - simula jogo azar sem dinheiro real -> 12+ Teen
- [ ] Público-alvo: 18+
- [ ] Teste interno: adicionar 20 emails testers (amigos, família)

### 3.4 Produtos In-App
- [ ] Monetização > Produtos > Criar assinatura mensal R$19,90
- [ ] Criar anual R$99,90 com 3 dias trial
- [ ] Criar produto único vitalício R$199,90

### 3.5 Upload AAB Teste Interno
- [ ] Teste interno > Criar nova versão > Upload app-release.aab
- [ ] Preencher notas: "Primeira versão com IA completa"
- [ ] Salvar e revisar > Iniciar lançamento teste interno
- [ ] Aguardar Google revisar (poucas horas)

---

## Dia 3-17: Teste Interno 14 Dias Obrigatório

**Google exige para novos desenvolvedores:** 20 testers, 14 dias contínuos, app instalado e usado.

- [ ] Enviar link teste interno para 20 pessoas
- [ ] Pedir para instalarem, gerarem matriz, usarem 5 min por dia
- [ ] Monitorar Play Console > Teste interno > Testers, ver se 20 ativos
- [ ] Monitorar Crashlytics (se Firebase configurado)
- [ ] Corrigir bugs que aparecerem, subir nova AAB se necessário (mantém contador 14 dias? Não, reinicia se nova AAB, então evitar subir nova nos 14 dias a menos que crítico)

**Enquanto teste interno roda (14 dias), fazer:**

### Backend (Dia 4-5)
- [ ] Deploy API `main_real.py` no Cloud Run
- [ ] Configurar Redis cache sorteios TTL 6h
- [ ] Cron 3x/semana puxa Caixa

### Firebase (Dia 6)
- [ ] Criar projeto Firebase lotofacil-pro
- [ ] Adicionar Android app com package com.berger33.lotofacilpro
- [ ] Baixar google-services.json para android/app/
- [ ] Ativar Analytics, Crashlytics, Remote Config, Messaging
- [ ] Configurar AdMob com IDs produção (trocar teste IDs)

### Monetização UI (Dia 7-8)
- [ ] Integrar BannerAdWidget real no dashboard e ranking
- [ ] Interstitial a cada 3 gerações (já tem lógica shouldShow)
- [ ] Rewarded para +20 gerações
- [ ] Paywall com IAPService real (buyMonthly, buyYearly, buyLifetime)
- [ ] Restaurar compras

### Polimento (Dia 9-10)
- [ ] Testes em 5 devices físicos (low-end a high-end)
- [ ] Performance: cold start <2s, geração 10 jogos <5s
- [ ] Acessibilidade: TalkBack, contraste, 48dp
- [ ] Haptic feedback, animações 60fps
- [ ] Empty states, error retry, offline indicator

---

## Dia 17: Beta Fechado -> Aberto -> Produção

### Após 14 dias teste interno OK
- [ ] Promover para Teste fechado > 100 testers (opcional)
- [ ] Depois Teste aberto > 500 testers (opcional, mas recomendado)
- [ ] Monitorar reviews, crashes, ANRs

### Produção Rollout Gradual
- [ ] Produção > Criar nova versão > Upload mesma AAB do teste interno (ou nova com correções)
- [ ] Rollout 20% > monitorar 24h Crashlytics
- [ ] Rollout 50% > 24h
- [ ] Rollout 100%

---

## Dia 18+: Crescimento

- [ ] Responder reviews <24h nos primeiros 30 dias (crítico para ranking)
- [ ] ASO Experiments: testar ícone, screenshots, descrição curta
- [ ] Google UAC campanha R$50/dia
- [ ] Blog SEO: "Dezenas quentes da semana" com análise
- [ ] Comunidade Telegram/Discord para Pro
- [ ] Roadmap: widget Android, notificações sorteios, ranking global, iOS

---

## Checklist Final Antes de Produção

- [ ] AAB assinado, targetSdk 34, minSdk 24, 64-bit
- [ ] Ícone 512, feature 1024x500, 5+ screenshots 1080x1920, vídeo 30s
- [ ] Descrição curta 80 chars, longa 4000 com keywords, disclaimer legal
- [ ] Privacy Policy URL pública
- [ ] Data Safety preenchido
- [ ] Content rating 12+
- [ ] Categoria Tools, não Gambling
- [ ] Sem permissão desnecessária (só INTERNET, BILLING, POST_NOTIFICATIONS)
- [ ] Sem promessa "ganhe dinheiro", só "análise estatística"
- [ ] Teste interno 20 testers 14 dias completo
- [ ] Produtos IAP criados e ativos
- [ ] AdMob IDs produção (não teste)
- [ ] Firebase Crashlytics sem crashes
- [ ] App Bundle <150MB (Flutter ~20MB OK)
- [ ] Cold start <2s, geração <5s

---

## Comandos Rápidos

```bash
# Gerar AAB
cd android_app/flutter_pro && flutter build appbundle --release

# Ver tamanho
ls -lh build/app/outputs/bundle/release/

# Testar em device
flutter install

# Logs
adb logcat | grep flutter

# Deploy API
cd android_app/api && gcloud run deploy lotofacil-api --source . --region us-central1 --allow-unauthenticated
```
