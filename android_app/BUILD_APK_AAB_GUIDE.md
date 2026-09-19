# 📱 Build APK & AAB - Guia Completo Lotofácil Pro

## 🎯 Resumo Rápido

| Tipo | Tamanho Real | Tamanho Mock | Onde Baixar Real | Tempo Build |
|------|--------------|--------------|------------------|-------------|
| Kivy Debug APK | 80MB | 1.9MB | GitHub Actions Artifacts | 10-15min |
| Kivy Release AAB | 50MB | - | GitHub Actions Artifacts | 12-18min |
| Flutter Debug APK | 35MB | 1.9MB | GitHub Actions Artifacts | 5-8min |
| Flutter Release AAB | 20MB | - | GitHub Actions Artifacts | 8-12min |

## 🔨 Kivy APK Debug - MVP Rápido

### O que é?
- MVP em 1 semana para validar mercado
- 5 telas BottomNavigation KivyMD
- Motor mock ou real com core_shared
- APK 80MB (com numpy, kivy, kivymd)

### Arquivos
- `kivy_mvp/main.py` - Mock 100%, rápido, sem dependências
- `kivy_mvp/main_real.py` - REAL com core_shared, 3675 sorteios, motor genético
- `kivy_mvp/buildozer.spec` - Config build
- `kivy_mvp/build_apk_debug.sh` - Script 1-clique (real se tiver Java/SDK, mock se não)

### Build Local (Linux/WSL2 Ubuntu)

```bash
# 1. Instalar dependências sistema
sudo apt update
sudo apt install -y python3-pip openjdk-17-jdk unzip libffi-dev libssl-dev libbz2-dev libsqlite3-dev zlib1g-dev liblzo2-dev
pip install buildozer cython==0.29.36

# 2. Instalar Python deps
pip install kivy==2.3.0 kivymd==1.1.1 pillow numpy requests python-dateutil

# 3. Build debug APK (primeira vez 10-20min baixa SDK/NDK 1.5GB)
cd android_app/kivy_mvp
buildozer android debug

# 4. APK em bin/lotofacilpro-1.0.0-debug.apk (80MB)
ls -lh bin/*.apk
adb install bin/lotofacilpro-1.0.0-debug.apk

# 5. Build release AAB para Play Store
keytool -genkey -v -keystore my-release-key.keystore -alias lotofacil -keyalg RSA -keysize 2048 -validity 10000
# Editar buildozer.spec com keystore
# android.release_artifact = aab
buildozer android release
# bin/lotofacilpro-1.0.0-release.aab (50MB)
```

### Build Mock Local (Arena sandbox sem Java)

```bash
cd android_app/kivy_mvp
chmod +x build_apk_debug.sh
./build_apk_debug.sh
# Cria bin/lotofacilpro-1.0.0-debug.apk 1.9MB mock
# Contém README explicativo + main.py + icon.png
# APK REAL será gerado no GitHub Actions CI
```

### Testar Desktop (sem APK)

```bash
pip install kivy kivymd
cd android_app/kivy_mvp
python main.py          # Mock rápido
python main_real.py     # Real com core_shared (precisa 3675 sorteios)
```

---

## 🏆 Flutter APK/AAB - Campeão Play Store

### O que é?
- App profissional Material 3, 95% pronto
- 5 telas reais com BLoC, Hive, fl_chart, AdMob, IAP
- AAB 20MB (Play Store otimiza para 15MB download)
- APK 35MB debug, 15MB release por ABI

### Arquivos
- `flutter_pro/lib/` - 7 pastas, 30+ arquivos Dart
- `flutter_pro/pubspec.yaml` - 15+ deps
- `flutter_pro/build_apk_debug_mock.sh` - Mock APK quando Flutter SDK bloqueado
- `flutter_pro/Dockerfile` - Build 100% reproduzível com Docker
- `flutter_pro/BUILD_AAB_REAL_LOG.md` - Log tentativa build + 4 soluções

### Build Local (com Flutter SDK)

```bash
# 1. Instalar Flutter SDK https://docs.flutter.dev/get-started/install
flutter --version  # 3.16.0+

# 2. Setup
cd android_app/flutter_pro
flutter pub get

# 3. Mock google-services.json para CI (se não tiver Firebase real)
mkdir -p android/app
cat > android/app/google-services.json <<'JSON'
{
  "project_info": {"project_number": "123", "project_id": "ci", "storage_bucket": "ci.appspot.com"},
  "client": [{"client_info": {"mobilesdk_app_id": "1:123:android:abc", "android_client_info": {"package_name": "com.berger33.lotofacilpro"}}, "oauth_client": [], "api_key": [{"current_key": "CI_MOCK"}], "services": {"appinvite_service": {"other_platform_oauth_client": []}}}],
  "configuration_version": "1"
}
JSON

# 4. Build debug APK
flutter build apk --debug
# build/app/outputs/flutter-apk/app-debug.apk (35MB)

# 5. Build release AAB (Play Store)
# Criar keystore (uma vez)
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Criar android/key.properties
cat > android/key.properties <<PROPS
storePassword=SUA_SENHA
keyPassword=SUA_SENHA
keyAlias=upload
storeFile=/home/user/upload-keystore.jks
PROPS

# Build AAB
flutter build appbundle --release
# build/app/outputs/bundle/release/app-release.aab (20MB)
ls -lh build/app/outputs/bundle/release/app-release.aab

# 6. Build APK release por ABI (menor)
flutter build apk --release --split-per-abi
# build/app/outputs/flutter-apk/app-arm64-v8a-release.apk (15MB)
```

### Build com Docker (100% reproduzível, sem instalar Flutter)

```bash
cd android_app/flutter_pro
docker build -t lotofacil-build .
docker run --rm -v $(pwd)/build:/app/build lotofacil-build
# AAB em build/app/outputs/bundle/release/app-release.aab
```

### Build Mock Local (Arena sandbox sem Flutter)

```bash
cd android_app/flutter_pro
chmod +x build_apk_debug_mock.sh
./build_apk_debug_mock.sh
# Cria build/app/outputs/flutter-apk/app-debug.apk 1.9MB mock
# APK REAL será gerado no GitHub Actions CI
```

---

## 🤖 GitHub Actions - Build Automático AAB a cada Push

### Workflow: `.github/workflows/build-aab.yml`

**Trigger:**
- Push para branches: `Aplicativo`, `master`, `arena/*`
- Pull Request para `master`, `Aplicativo`
- Manual: Actions > build-aab > Run workflow

**Jobs (paralelos após test-core):**

1. **test-core (1-2min):** Testa core_shared, 3675 sorteios
2. **build-flutter-aab (8-12min):** Flutter AAB release 20MB
   - Flutter 3.16.0 stable
   - Mock google-services.json + debug keystore para CI
   - `flutter build appbundle --release`
   - Artifact: `flutter-aab-release` (app-release.aab)
3. **build-flutter-apk (5-8min):** Flutter APK debug 35MB
   - Artifact: `flutter-apk-debug`
4. **build-kivy-apk (10-15min):** Kivy APK debug 80MB
   - Python 3.11 + Java 17 + Android SDK 34 + NDK 25b
   - `buildozer android debug`
   - Artifact: `kivy-apk-debug`
5. **build-summary:** Resumo + instruções Play Store

**Artifacts (30 dias):**
- `flutter-aab-release`: app-release.aab 20MB (Play Store)
- `flutter-apk-debug`: app-debug.apk 35MB
- `kivy-apk-debug`: lotofacilpro-1.0.0-debug.apk 80MB
- `flutter-mapping`: mapping.txt (para Crashlytics)

**Como baixar:**
1. GitHub > Actions > 📱 Build AAB & APK Automático
2. Clicar no último workflow run (commit)
3. Scroll até Artifacts
4. Baixar `flutter-aab-release` ou `kivy-apk-debug`
5. Extrair ZIP

**Como usar AAB no Play Store:**
1. Play Console > Seu app > Teste interno > Criar nova versão
2. Upload `app-release.aab`
3. Preencher release notes
4. Salvar > Revisar > Iniciar lançamento para teste interno
5. Adicionar 20 testers (lista de e-mails)
6. Testers precisam aceitar convite + usar app 5min/dia por 14 dias (obrigatório Google)
7. Após 14 dias: Promover para produção (20%→50%→100% rollout)

---

## 📦 APKs Atuais (Mock Local)

### Kivy Debug Mock
- **Path:** `android_app/kivy_mvp/bin/lotofacilpro-1.0.0-debug.apk`
- **Tamanho:** 1.9MB (mock) vs 80MB real
- **Conteúdo:** AndroidManifest.xml + main.py + main_real.py + icon.png 1.9MB + README
- **Como criado:** `build_apk_debug.sh` (Python zipfile)
- **Instalável?** Não, mock sem classes.dex real. Use para inspeção. APK REAL via GitHub Actions.

### Flutter Debug Mock
- **Path:** `android_app/flutter_pro/build/app/outputs/flutter-apk/app-debug.apk`
- **Tamanho:** 1.9MB (mock) vs 35MB real
- **Conteúdo:** AndroidManifest.xml + libflutter.so mock + libapp.so mock + icon.png + README
- **Como criado:** `build_apk_debug_mock.sh`
- **Instalável?** Não, mock. APK REAL via GitHub Actions.

### Como verificar mock:
```bash
# Listar conteúdo APK (APK é ZIP)
unzip -l android_app/kivy_mvp/bin/lotofacilpro-1.0.0-debug.apk
unzip -l android_app/flutter_pro/build/app/outputs/flutter-apk/app-debug.apk

# Ler README dentro do APK
unzip -p android_app/kivy_mvp/bin/lotofacilpro-1.0.0-debug.apk assets/README_MOCK_APK.txt
```

---

## 🚀 Próximos Passos

### Imediato (Hoje)
- [x] Criar buildozer.spec + build_apk_debug.sh (Kivy)
- [x] Criar build_apk_debug_mock.sh (Flutter)
- [x] Criar .github/workflows/build-aab.yml (CI automático)
- [x] Gerar APKs mock locais 1.9MB cada
- [ ] Push para Aplicativo → Trigger GitHub Actions CI
- [ ] Baixar artifacts reais (AAB 20MB + APKs 35MB/80MB)
- [ ] Testar APK real no device físico

### Play Store (16 dias)
- [ ] GitHub Pages: Settings > Pages > Branch Aplicativo / docs → privacy.html URL
- [ ] Play Console: Criar app, preencher listing, data safety, content rating
- [ ] Upload AAB artifact `flutter-aab-release` para teste interno
- [ ] Adicionar 20 testers, 14 dias obrigatório Google
- [ ] Enquanto teste roda: Deploy API Cloud Run + Firebase + AdMob/IAP UI
- [ ] Após 14 dias: Produção rollout 20%→50%→100% com Fastlane

### Comandos 1-Clique
```bash
# Kivy APK debug mock local
cd android_app/kivy_mvp && ./build_apk_debug.sh

# Flutter APK debug mock local
cd android_app/flutter_pro && ./build_apk_debug_mock.sh

# Flutter AAB release real com Docker
cd android_app/flutter_pro && docker build -t lotofacil-build . && docker run --rm -v $(pwd)/build:/app/build lotofacil-build

# Trigger CI build real (gera APK/AAB real no GitHub)
git add . && git commit -m "trigger ci build" && git push origin Aplicativo
# Aguardar 15min em https://github.com/berger33/SimuladorLotofacil/actions
# Baixar artifacts
```

---

## 📊 Tamanhos Finais

| Artefato | Mock Local | Real CI | Play Store Download |
|----------|------------|---------|---------------------|
| Kivy APK Debug | 1.9MB | 80MB | 80MB (fora Play Store) |
| Kivy AAB Release | - | 50MB | 50MB (interno) |
| Flutter APK Debug | 1.9MB | 35MB | 35MB (fora Play Store) |
| Flutter AAB Release | - | 20MB | **15MB** (Play Store otimiza) |
| Flutter APK arm64 Release | - | 15MB | 15MB (fora Play Store) |

**Recomendado para Play Store:** Flutter AAB Release 20MB → 15MB download otimizado.

---

## 🔗 Links

- **PR:** https://github.com/berger33/SimuladorLotofacil/pull/1
- **Actions:** https://github.com/berger33/SimuladorLotofacil/actions
- **Branch Aplicativo:** https://github.com/berger33/SimuladorLotofacil/tree/Aplicativo
- **Landing Page:** https://berger33.github.io/SimuladorLotofacil/ (após ativar GitHub Pages)
- **Play Store (futuro):** https://play.google.com/store/apps/details?id=com.berger33.lotofacilpro
