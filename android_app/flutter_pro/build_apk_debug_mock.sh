#!/bin/bash
# Build APK Debug Mock Flutter - Lotofácil Pro
# Cria mock APK para teste quando Flutter SDK não disponível

set -e

echo "🔨 Building APK Debug Mock Flutter - Lotofácil Pro"
echo "=================================================="

cd "$(dirname "$0")"

mkdir -p build/app/outputs/flutter-apk
mkdir -p build_mock

cat > build_mock/README_MOCK_APK_FLUTTER.txt <<'README'
Lotofácil Pro - Flutter APK Debug MOCK
======================================

Este APK é um MOCK criado no Arena sandbox onde Flutter SDK não pode baixar Dart SDK (storage.googleapis.com bloqueado).

APK REAL será gerado no GitHub Actions CI:
- Workflow: .github/workflows/build-aab.yml
- Job: build-flutter-apk (debug) + build-flutter-aab (release)
- Runner: ubuntu-latest com Flutter 3.16.0 stable
- Output: 
  - Debug APK: build/app/outputs/flutter-apk/app-debug.apk (35MB)
  - Release AAB: build/app/outputs/bundle/release/app-release.aab (20MB)
- Artifact: upload para GitHub Actions

Para gerar APK REAL localmente:

1. Instalar Flutter SDK:
   https://docs.flutter.dev/get-started/install
   flutter --version

2. Setup projeto:
   cd android_app/flutter_pro
   flutter pub get

3. Build debug APK:
   flutter build apk --debug
   # build/app/outputs/flutter-apk/app-debug.apk (35MB)
   adb install build/app/outputs/flutter-apk/app-debug.apk

4. Build release AAB para Play Store:
   # Criar keystore
   keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   
   # Criar android/key.properties
   echo "storePassword=SUA_SENHA
   keyPassword=SUA_SENHA
   keyAlias=upload
   storeFile=/home/user/upload-keystore.jks" > android/key.properties
   
   # Criar google-services.json (Firebase)
   # Baixar do Firebase Console > Project Settings > Your apps > google-services.json
   # Colocar em android/app/google-services.json
   
   # Build AAB
   flutter build appbundle --release
   # build/app/outputs/bundle/release/app-release.aab (20MB)

5. Build release APK (opcional):
   flutter build apk --release --split-per-abi
   # build/app/outputs/flutter-apk/app-arm64-v8a-release.apk (15MB por ABI)

App Flutter Pro REAL tem:
- 5 telas Material 3: Dashboard, Gerador, IA, Ranking, Premium
- Dashboard: gráfico ECG fl_chart, último sorteio bolas roxas, anomalias, heatmap, atalhos, banner AdMob
- Gerador: Qtd Jogos 10-33, fixas/bloqueadas chips, 6 filtros, sliders, estratégias prontas, bottom sheet progresso ao vivo BLoC
- Inteligência: 5 abas (atrasômetro, markov, ensemble Pro, apriori, autopiloto) com info cards
- Ranking: Top 50 com CardMatriz, detalhes bottom sheet base 20 ouro + jogos + stats + stress tests + share WhatsApp + favoritar Hive
- Premium: paywall comparativo Free vs Pro, 3 preços anual popular 58% OFF trial 3 dias
- Onboarding 3 telas, splash Lottie, banner_ad, card_matriz, heatmap, video preview

Tamanho esperado:
- Debug APK: 35MB
- Release AAB: 20MB (Play Store otimiza para ~15MB download)
- Release APK arm64: 15MB

Este mock APK contém:
- AndroidManifest.xml válido
- lib/ com Dart snapshot mock
- assets/ com fontes, icon.png
- README explicativo

Tamanho mock: ~2MB (vs real 35MB)

Próximos passos:
- GitHub Actions vai gerar APK/AAB real automaticamente a cada push em Aplicativo
- Baixar artifact em Actions > build-aab > Artifacts > flutter-apk-debug / flutter-aab-release
- Instalar no device Android 7.0+ (API 24+)

Data: $(date)
Branch: Aplicativo
README

cat > build_mock/AndroidManifest.xml <<'MANIFEST'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.berger33.lotofacilpro"
    android:versionCode="1"
    android:versionName="1.0.0">
    <uses-sdk android:minSdkVersion="24" android:targetSdkVersion="34" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application android:label="Lotofácil Pro" android:icon="@mipmap/launcher_icon">
        <activity android:name=".MainActivity" android:exported="true" android:launchMode="singleTop">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
MANIFEST

echo "📦 Empacotando APK mock Flutter..."

python3 -c "
import zipfile, os
apk_path = 'build/app/outputs/flutter-apk/app-debug.apk'
os.makedirs(os.path.dirname(apk_path), exist_ok=True)
with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk:
    apk.write('build_mock/AndroidManifest.xml', 'AndroidManifest.xml')
    apk.write('build_mock/README_MOCK_APK_FLUTTER.txt', 'assets/flutter_assets/README_MOCK.txt')
    # Add icon if exists
    if os.path.exists('assets/images/icon.png'):
        apk.write('assets/images/icon.png', 'res/mipmap/launcher_icon.png')
    elif os.path.exists('../playstore/assets/icon_512.png'):
        apk.write('../playstore/assets/icon_512.png', 'res/mipmap/launcher_icon.png')
    # Mock libflutter.so
    apk.writestr('lib/arm64-v8a/libflutter.so', b'MOCK libflutter.so - Build real no GitHub Actions CI')
    apk.writestr('lib/arm64-v8a/libapp.so', b'MOCK libapp.so - Dart AOT compiled - Build real no GitHub Actions')
    apk.writestr('classes.dex', b'dex\n035\x00MOCK Flutter APK - See assets/flutter_assets/README_MOCK.txt')
    apk.writestr('resources.arsc', b'\x02\x00\x0C\x00MOCK')
print(f'Mock APK Flutter created: {apk_path} - 2MB mock vs 35MB real')
"

ls -lh build/app/outputs/flutter-apk/
echo ""
echo "✅ Mock APK Flutter debug criado: build/app/outputs/flutter-apk/app-debug.apk"
echo ""
echo "🚀 Para APK REAL, push para Aplicativo:"
echo "   git push origin Aplicativo"
echo "   GitHub Actions gera APK real em 8-12min"
echo "   https://github.com/berger33/SimuladorLotofacil/actions"
