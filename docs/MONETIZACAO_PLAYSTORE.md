# 💰 MONETIZAÇÃO E PLAY STORE - Estratégia Comercial Completa

## 1. Modelo de Negócio: Freemium + Ads + Subscription

### Por que Freemium para Lotofácil?
- Usuário de loteria é desconfiado, precisa testar grátis antes de pagar
- Play Store favorece apps com baixa barreira de entrada
- Ads monetizam 95% que nunca pagariam, subscription monetiza 5% heavy users

### Tabela Free vs Pro

| Feature | Free | Pro Mensal R$19,90 | Pro Anual R$99 (58% off) | Vitalício R$199 |
|---------|------|-------------------|--------------------------|-----------------|
| Qtd Jogos | 10 | 33 | 33 | 33 |
| Gerações por execução | 50 | Ilimitado | Ilimitado | Ilimitado |
| Atrasômetro | ✅ | ✅ | ✅ | ✅ |
| Markov | ✅ | ✅ | ✅ | ✅ |
| Ensemble Híbrido | ❌ | ✅ | ✅ | ✅ |
| Apriori Combos Ouro | ❌ | ✅ | ✅ | ✅ |
| Auto-Piloto XGBoost | ❌ | ✅ | ✅ | ✅ |
| RL Agent Autônomo | ❌ | ✅ | ✅ | ✅ |
| Foco 14 Cofre Seguro | ✅ | ✅ | ✅ | ✅ |
| Filtros avançados | 3 | Todos | Todos | Todos |
| Turbo | ❌ | ✅ | ✅ | ✅ |
| Stress Tests | 1 (histórico) | 3 | 3 | 3 |
| Export CSV/PDF | ❌ | ✅ | ✅ | ✅ |
| Compartilhar WhatsApp | ✅ com marca d'água | ✅ sem marca | ✅ | ✅ |
| Ranking Top 50 | Top 10 | Top 50 | Top 50 | Top 50 |
| Snapshots | 1 | Ilimitado | Ilimitado | Ilimitado |
| Anúncios | Banner + Interstitial | Sem ads | Sem ads | Sem ads |
| Suporte | Comunidade | Prioritário | Prioritário | VIP |
| Notificações sorteio | ❌ | ✅ | ✅ | ✅ |

### Psicologia de Preço
- **Âncora:** Vitalício R$199 parece caro, faz anual R$99 parecer barato (R$8,25/mês)
- **Decoy:** Mensal R$19,90 existe para fazer anual parecer negócio, mas alguns vão assinar mensal por impulso
- **Trial:** 3 dias grátis no anual, sem cartão? Com cartão mas cancela fácil (Play Store exige)
- **Paywall timing:** Mostrar após 2 gerações free + quando tenta usar feature pro (contextual)

## 2. Implementação Técnica Monetização

### 2.1 AdMob (google_mobile_ads)

**Formatos:**
- **Banner:** Dashboard bottom, Ranking bottom - sempre visível free
  - ID: ca-app-pub-xxx/banner_dashboard
  - Refresh 30s
- **Interstitial:** A cada 3 gerações completadas ou a cada 2 stress tests
  - Não mostrar nos primeiros 5 minutos (evita churn)
  - Mostrar após salvar matriz (momento de dopamina)
- **Rewarded:** "Assista um vídeo para liberar +20 gerações ou desbloquear Ensemble 1x"
  - Conversão alta, usuário escolhe ver
  - Limite 3 por dia para não canibalizar pro

**Código Flutter:**
```dart
class AdsService {
  BannerAd? _banner;
  InterstitialAd? _interstitial;
  RewardedAd? _rewarded;
  int _geracoesDesdeUltimoInterstitial = 0;

  Future<void> init() async {
    await MobileAds.instance.initialize();
  }

  BannerAd createBanner() {
    return BannerAd(
      adUnitId: AdHelper.bannerAdUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(),
    )..load();
  }

  bool shouldShowInterstitial() {
    _geracoesDesdeUltimoInterstitial++;
    if (_geracoesDesdeUltimoInterstitial >= 3) {
      _geracoesDesdeUltimoInterstitial = 0;
      return true;
    }
    return false;
  }

  Future<void> showInterstitial() async {
    // load + show
  }

  Future<bool> showRewarded() async {
    // retorna true se completou
  }
}
```

**eCPM estimado Brasil:**
- Banner: $0.20 - $0.50
- Interstitial: $1.00 - $3.00
- Rewarded: $3.00 - $8.00
- Com 10k DAU free, 3 interstitial/dia = ~$150-300/dia só interstitial

### 2.2 In-App Purchase (in_app_purchase)

**Produtos no Play Console:**
- `lotofacil_pro_monthly` - subscription mensal R$19,90 - 1 mês
- `lotofacil_pro_yearly` - subscription anual R$99,90 - 1 ano com 3 dias trial
- `lotofacil_pro_lifetime` - in-app não consumível R$199,90 - vitalício

**Implementação:**
```dart
class IAPService {
  final _inAppPurchase = InAppPurchase.instance;
  bool _isPremium = false;

  Future<void> init() async {
    final available = await _inAppPurchase.isAvailable();
    if (!available) return;

    // Listener de compras
    _inAppPurchase.purchaseStream.listen(_onPurchase);

    // Restore
    await _inAppPurchase.restorePurchases();

    // Checa status
    _isPremium = await _checkPremium();
  }

  Future<bool> isPremium() async {
    // checa local + valida no backend (opcional)
    return _isPremium || await _validateServer();
  }

  Future<void> buyMonthly() async {
    final product = await _getProduct('lotofacil_pro_monthly');
    final purchaseParam = PurchaseParam(productDetails: product);
    await _inAppPurchase.buyNonConsumable(purchaseParam: purchaseParam);
  }

  void _onPurchase(List<PurchaseDetails> purchases) {
    for (var purchase in purchases) {
      if (purchase.status == PurchaseStatus.purchased) {
        // valida receipt no backend (importante anti-fraude)
        _deliverPremium(purchase);
        _inAppPurchase.completePurchase(purchase);
      }
    }
  }
}
```

**Validação servidor (anti-crack):**
- Enviar purchase token para FastAPI backend
- Backend valida com Google Play Developer API
- Salva no Firestore: user_id -> premium_until
- Flutter checa local + remote

### 2.3 Estratégia Paywall

**Quando mostrar:**
1. App start (após onboarding) - soft paywall "Conheça o Pro" com X para fechar
2. Ao tentar gerar >10 jogos
3. Ao clicar em Ensemble, Apriori, Auto-Piloto
4. Após 2 gerações free: "Você gerou 2 matrizes grátis, desbloqueie ilimitado"
5. Ao tentar exportar
6. A cada 5 aberturas do app (não irritar)

**Design paywall (alta conversão):**
- Título: "Desbloqueie o Potencial Máximo 🚀"
- Sub: "Junte-se a 1.200+ jogadores Pro"
- Lista benefícios com checkmarks
- Depoimentos falsos? Não, usar reviews reais após beta
- Preços com destaque no anual: "MAIS POPULAR" badge
- Botão CTA grande: "Começar 3 dias grátis"
- Texto pequeno: "Cancele a qualquer momento"
- Link: Restaurar compras, Termos, Privacy

## 3. Play Store - ASO e Compliance

### 3.1 Compliance Jogo de Azar (Crítico)

Google Play tem política rígida para gambling. Nosso app NÃO é gambling, é ferramenta educacional.

**O que fazer:**
- **Categoria:** Tools ou Education (não Entertainment, não Gambling)
- **Tags:** lotofacil, estatística, análise, desdobramento, inteligência artificial
- **Descrição NÃO pode conter:**
  - "Ganhe dinheiro", "Fique rico", "Garantia de prêmio", "Aposte"
  - Usar: "Análise estatística", "Simulação", "Estudo", "Ferramenta educacional", "Não garante ganhos"
- **Disclaimer obrigatório na descrição + onboarding + dentro do app:**
  > "AVISO LEGAL: Este aplicativo é uma ferramenta de análise estatística e simulação educacional. Não é afiliado à Caixa Econômica Federal. Loteria é jogo de azar com resultados independentes. Este app não garante prêmios ou lucros. Jogue com responsabilidade. +18. Se você tem problemas com jogo, procure ajuda: www.jogoresponsavel.org.br"

- **Classificação etária:** Questionário IARC
  - Simula jogo de azar? Sim, mas sem dinheiro real -> 12+ ou Teen
  - Não pode ser Everyone

- **Data Safety:**
  - Coleta dados? Sim: analytics anonimizado (Firebase), crash logs, ID de dispositivo para ads
  - Compartilha? Sim com Google (AdMob, Firebase)
  - Criptografia? Sim em trânsito
  - Usuário pode deletar dados? Sim (botão deletar conta)

### 3.2 Assets Play Store

**Ícone (512x512):**
- Fundo roxo gradiente #6F42C1 -> #4A1A8B
- Símbolo: trevo ou gráfico + números 01 02 com estilo tech
- Sem texto, sem borda, Material icon guidelines

**Feature Graphic (1024x500):**
- Título: "Lotofácil Pro - IA & Estatística"
- Sub: "Desdobramentos Inteligentes"
- Visual: heatmap + gráfico + mockup celular
- Sem texto muito pequeno

**Screenshots (min 2, max 8, 1080x1920 ou 1440x2560):**
1. Dashboard com gráfico e lucro
2. Gerador com filtros e sliders
3. Inteligência com heatmap e Top 5
4. Ranking com cards matrizes
5. Detalhes matriz com jogos
6. Tela Premium comparativo
7. Onboarding
8. Stress test resultado

**Vídeo preview (30-60s):**
- Screen recording com narração: "Transforme 20 dezenas em 15 jogos inteligentes com IA"

**Descrição curta (80 chars):**
"IA para Lotofácil: desdobramentos, estatísticas e análises inteligentes"

**Descrição longa (4000 chars) com SEO:**
```
🎰 Lotofácil Pro - O Laboratório de Inteligência Artificial para Análise da Lotofácil

Cansado de jogar no escuro? O Lotofácil Pro é uma ferramenta educacional de análise estatística que usa Algoritmo Genético, Machine Learning e Estatística Avançada para criar desdobramentos inteligentes.

✨ O QUE VOCÊ ENCONTRA:

🧬 ALGORITMO GENÉTICO
Evolução de matrizes. As melhores sobrevivem, cruzam e mutam. A cada geração, o lucro médio aumenta.

🤖 INTELIGÊNCIA ARTIFICIAL
- Atrasômetro: desvio padrão e ruptura de dezenas
- Cadeias de Markov: sinergia entre números
- Ensemble Híbrido (Conselho Jedi): XGBoost + Markov + Atraso elegem Top 5 dezenas
- Mineração Apriori: trincas que mais saem juntas
- Auto-Piloto: prevê soma, ímpares, primos automaticamente
- IA Autônoma (DQN): rede neural que auto-calibra mutação

🎯 FECHAMENTO INTELIGENTE
Transforme 20 dezenas em 15 jogos com filtros: ímpares, moldura, primos, soma, Fibonacci, sequências. Sistema com relaxamento automático para nunca travar.

📊 PROVAS DE FOGO
Teste suas matrizes contra histórico real, 100k sorteios caóticos ou bootstrap hipergeométrico. Veja ROI, acertos 11-15.

🏆 RANKING E GESTÃO
Salve top 50 matrizes, snapshots, gestão de banca com alerta de drawdown, export CSV/PDF, compartilhe no WhatsApp.

🎨 DESIGN PROFISSIONAL
Modo claro/escuro, heatmap sensorial, gráficos de convergência, interface moderna Material 3.

⚠️ AVISO LEGAL IMPORTANTE
Ferramenta educacional de simulação estatística. Não afiliado à Caixa. Loteria é jogo de azar, resultados independentes, sem garantia de prêmios. Jogue com responsabilidade. +18.

🔓 VERSÃO FREE E PRO
Free: 10 jogos, análises básicas, com anúncios.
Pro: 33 jogos, IA completa, ilimitado, sem anúncios, export, suporte prioritário.

Baixe agora e leve sua análise para o próximo nível!

Palavras-chave: lotofácil, lotofacil, desdobramento, fechamento, análise lotofácil, estatística lotofácil, inteligência artificial loteria, simulador lotofácil, palpite lotofácil (para ASO, mas cuidado: palpite pode ser considerado gambling, usar com moderação)
```

### 3.3 Checklist Lançamento

- [ ] Conta Google Play Developer (US$25)
- [ ] App Bundle assinado com keystore (guardar!)
- [ ] Privacy Policy hospedada (GitHub Pages: berger33.github.io/SimuladorLotofacil/privacy)
- [ ] Terms of Service
- [ ] Data Safety preenchido
- [ ] Content rating IARC
- [ ] Target API 34, compile 34
- [ ] 64-bit, App Bundle
- [ ] Testes internos (min 20 testers 14 dias) - obrigatório para novos devs 2024+
- [ ] Closed testing
- [ ] Open testing (opcional)
- [ ] Produção com rollout gradual 20% -> 50% -> 100%
- [ ] Crashlytics e Analytics desde dia 1
- [ ] Resposta rápida a reviews negativos (primeiras 48h críticas)

## 4. Métricas e Crescimento

### KPIs para acompanhar
- **Aquisição:** Impressões Play Store, CTR, Instalações, Custo por instalação (se ads)
- **Ativação:** % que completa onboarding, % que gera 1ª matriz
- **Retenção:** D1, D7, D30 (meta: 40%, 20%, 10%)
- **Receita:** ARPU, ARPPU, conversão free->pro (meta 3-5%), churn subscription, LTV
- **Engajamento:** Gerações por usuário, tempo no app, telas mais usadas

### Growth loops
- **Viral:** Compartilhar matriz no WhatsApp com link "Gerado com Lotofácil Pro"
- **Conteúdo:** Blog com análises semanais "Dezenas quentes da semana" -> SEO
- **Comunidade:** Telegram/Discord para usuários Pro
- **ASO:** Testar ícones, screenshots, descrições com Google Play Experiments

### Estimativa receita (conservadora)
- 10k instalações mês 1, 20% DAU = 2k DAU
- 5% conversão pro anual R$99 = 100 pagantes = R$9.900
- Ads: 2k DAU * 3 interstitial * R$2 eCPM /1000 = R$12/dia = R$360/mês
- Mês 1: ~R$10k
- Mês 6 com 100k instalações: ~R$100k/mês
- Mês 12 com 500k: ~R$500k/mês potencial

## 5. Riscos Monetização

- **Chargeback:** Usuário compra e pede reembolso Google (48h) -> perda, mas normal 2-5%
- **Crack:** App crackeado sem IAP -> mitigar com validação servidor
- **AdMob ban:** Se clicar próprio anúncio ou conteúdo enganoso -> nunca clicar próprio, seguir políticas
- **Play Store remove app por gambling:** Mitigar com disclaimer forte, categoria correta, sem promessa ganho

## 6. Próximos Passos Monetização

1. Criar contas AdMob e Play Console
2. Configurar produtos IAP no Play Console
3. Implementar AdsService e IAPService no Flutter
4. Criar backend validação receipt
5. Design paywall com alta conversão (inspirar em apps como TradingView, MyFitnessPal)
6. A/B testar preços: R$99 vs R$79 vs R$129 anual
