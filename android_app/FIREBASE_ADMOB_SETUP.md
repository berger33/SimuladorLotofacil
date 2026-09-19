# 🔥 Firebase + AdMob Setup - Guia Completo 15 minutos

## Firebase (Analytics, Crashlytics, Remote Config, Messaging)

### 1. Criar Projeto
- https://console.firebase.google.com > Criar projeto
- Nome: `lotofacil-pro`
- Google Analytics: Ativar (recomendado)
- Conta Analytics: Padrão

### 2. Adicionar Android App
- Firebase Console > Adicionar app > Android
- Package: `com.berger33.lotofacilpro` (deve bater com `android/app/build.gradle` applicationId)
- Apelido: Lotofácil Pro
- SHA-1: (opcional, para Auth) - `cd android && ./gradlew signingReport` pegar SHA-1 debug
- Baixar `google-services.json` e colocar em `android_app/flutter_pro/android/app/google-services.json`
- **NUNCA commitar google-services.json real** - está no .gitignore, usar .example como template

### 3. SDK Flutter
```bash
cd android_app/flutter_pro
dart pub global activate flutterfire_cli
flutterfire configure --project=lotofacil-pro
# Selecionar Android, iOS opcional
# Gera lib/firebase_options.dart automaticamente
```

### 4. Ativar Produtos Firebase Console

#### Analytics (grátis, essencial)
- Firebase > Analytics > Ativar
- Ver eventos automaticamente: screen_view, app_open, etc
- Criar eventos custom: `gerar_matriz`, `ver_ranking`, `clicar_premium`, `comprar_pro`

#### Crashlytics (grátis, essencial)
- Firebase > Crashlytics > Ativar
- Adicionar no `main_production.dart`:
```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
PlatformDispatcher.instance.onError = (error, stack) {
  FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
  return true;
};
```

#### Remote Config (grátis, feature flags)
- Firebase > Remote Config > Criar
- Parâmetros:
  - `max_jogos_free` = 10 (pode mudar para 15 sem atualizar app)
  - `enable_ensemble` = false (desativa se crash)
  - `paywall_anual_price` = 99.90 (A/B test preço)
  - `show_banner_ads` = true
- Buscar no app:
```dart
final remoteConfig = FirebaseRemoteConfig.instance;
await remoteConfig.fetchAndActivate();
int maxJogos = remoteConfig.getInt('max_jogos_free');
```

#### Messaging FCM (notificações)
- Firebase > Messaging > Ativar
- Criar notificação: "Seu ranking evoluiu! Nova matriz top 1"
- No Flutter:
```dart
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  // Mostrar notificação local
});
```

### 5. Verificar
```bash
flutter run
# Deve ver logs: Firebase initialized, Analytics enabled
# Firebase Console > Analytics > DebugView deve mostrar eventos
```

---

## AdMob (Monetização Free)

### 1. Criar Conta
- https://admob.google.com > Criar conta com mesma conta Google Play Developer
- Adicionar app: Android > com.berger33.lotofacilpro > Lotofácil Pro

### 2. Criar Unidades de Anúncio

#### Banner Dashboard
- AdMob > Apps > Lotofácil Pro > Criar unidade > Banner
- Nome: `lotofacil_dashboard_banner`
- Tipo: Banner adaptativo
- Salvar ID: `ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY`
- Trocar em `lib/services/ads_service.dart` bannerAdUnitId e `AndroidManifest.xml` APPLICATION_ID

#### Interstitial Geração
- Criar unidade > Intersticial
- Nome: `lotofacil_interstitial_geracao`
- Frequência: a cada 3 gerações (já implementado shouldShowInterstitial)
- ID: `ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY`

#### Rewarded +20 Gerações
- Criar unidade > Premiado
- Nome: `lotofacil_rewarded_extra`
- Recompensa: 20 gerações extra
- ID: `ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY`

### 3. Configurar no Código

#### AndroidManifest.xml
```xml
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/> <!-- App ID, não unit ID -->
```

#### ads_service.dart
```dart
static const String bannerAdUnitId = 'ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY'; // trocar teste ID
static const String interstitialAdUnitId = 'ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY';
static const String rewardedAdUnitId = 'ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY';
```

#### main_production.dart
```dart
await MobileAds.instance.initialize();
```

### 4. Teste

- Usar IDs teste Google durante desenvolvimento (já estão no código):
  - Banner teste: `ca-app-pub-3940256099942544/6300978111`
  - Interstitial teste: `ca-app-pub-3940256099942544/1033173712`
  - Rewarded teste: `ca-app-pub-3940256099942544/5224354917`
  - App ID teste: `ca-app-pub-3940256099942544~3347511713`

- Em produção, trocar para IDs reais AdMob
- AdMob Console > Configurações > Dispositivos de teste > Adicionar seu device ID (para ver ads reais sem violar política)

### 5. Políticas AdMob (Evitar Ban)

- ❌ NUNCA clicar nos próprios anúncios
- ❌ Não colocar banner perto de botão (clique acidental)
- ❌ Não mostrar interstitial ao abrir ou sair do app
- ❌ Não incentivar "Clique no anúncio para nos ajudar"
- ✅ Rewarded OK incentivar "Assista vídeo para liberar +20 gerações"
- ✅ Mostrar consent form GDPR se usuário na Europa (usar UMP SDK)

---

## Play Billing (IAP Premium)

### 1. Play Console > Monetização

#### Assinatura Mensal
- Criar assinatura > ID: `lotofacil_pro_monthly`
- Nome: Pro Mensal
- Descrição: Acesso completo por 1 mês
- Preço: R$19,90/mês
- Período faturamento: 1 mês
- Trial: nenhum
- Grupo: pro_subscription

#### Assinatura Anual (Mais Popular)
- ID: `lotofacil_pro_yearly`
- Nome: Pro Anual - Mais Popular
- Descrição: Acesso completo por 1 ano, 58% OFF
- Preço: R$99,90/ano
- Período: 1 ano
- Trial: 3 dias grátis
- Grupo: pro_subscription (mesmo grupo, anual é upgrade)

#### Produto Único Vitalício
- Produtos no app > Criar produto gerenciado
- ID: `lotofacil_pro_lifetime`
- Nome: Pro Vitalício
- Descrição: Pagamento único, acesso para sempre
- Preço: R$199,90
- Tipo: Não consumível

### 2. Código Flutter

Já implementado em `services/iap_service.dart`:
- `isPremium()` checa Hive
- `buyMonthly()`, `buyYearly()`, `buyLifetime()`
- `restore()` restaura compras
- `purchaseStream` listener valida e entrega premium

### 3. Validação Servidor (Anti-Crack)

Em produção, validar receipt no backend:

```dart
// No IAPService _deliverPremium
var token = purchase.verificationData.serverVerificationData;
var response = await Dio().post('https://api.lotofacilpro.com/api/v1/billing/validate', data: {
  'purchaseToken': token,
  'productId': purchase.productID,
});
if (response.data['valid']) {
  // Salva premium
}
```

Backend FastAPI:
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file('play-console-service-account.json')
service = build('androidpublisher', 'v3', credentials=credentials)
result = service.purchases().subscriptions().get(packageName='com.berger33.lotofacilpro', subscriptionId='lotofacil_pro_yearly', token=purchaseToken).execute()
# Verifica result['paymentState'] == 1 (pago)
```

### 4. Teste IAP

- Play Console > Configuração > Teste de licença > Adicionar emails testers
- Em device com email tester, usar cartão teste:
  - Teste aprovado, Teste recusado, etc: https://developer.android.com/google/play/billing/test
- Testar compra, restore, cancelamento

---

## Checklist Final Firebase+AdMob+IAP

- [ ] Firebase projeto criado, google-services.json em android/app/ (não commitado)
- [ ] flutterfire configure gerou firebase_options.dart
- [ ] Analytics DebugView mostra eventos
- [ ] Crashlytics sem crashes, teste forçar crash
- [ ] Remote Config com 4 parâmetros e fetch
- [ ] AdMob App ID em AndroidManifest.xml (produção, não teste)
- [ ] AdMob 3 unit IDs em ads_service.dart (produção)
- [ ] IAP 3 produtos criados no Play Console e ativos
- [ ] IAP testado com email tester e cartão teste
- [ ] Validação servidor implementada (opcional mas recomendado anti-crack)
- [ ] Consent form GDPR se necessário (UMP SDK)

---

## Custo

- Firebase: Spark free tier (Analytics, Crashlytics, Remote Config, Messaging grátis até limites)
- AdMob: Grátis, você recebe por ads
- Play Billing: Google fica com 15% (primeiro 1M USD/ano) ou 30%

## Tempo

- Firebase setup: 15 min
- AdMob setup: 15 min
- IAP setup: 30 min
- Total: 1 hora
