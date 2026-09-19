# 🔨 BUILD GUIDE - Como gerar APK/AAB

## Kivy MVP (Mais rápido - 1 semana)

### Desktop teste
```bash
cd android_app/kivy_mvp
pip install kivy kivymd numpy requests
python main.py          # mock
python main_real.py     # com core_shared real
```

### APK com Buildozer (Linux ou WSL2 Ubuntu)
```bash
# Instalar dependências sistema (Ubuntu)
sudo apt update
sudo apt install -y python3-pip openjdk-17-jdk unzip
pip install buildozer cython

# Build debug APK
cd android_app/kivy_mvp
buildozer android debug

# APK em bin/lotofacilpro-0.1-debug.apk
# Instalar no device
adb install bin/*.apk
```

### AAB para Play Store (release)
```bash
# Gerar keystore (uma vez)
keytool -genkey -v -keystore my-release-key.keystore -alias lotofacil -keyalg RSA -keysize 2048 -validity 10000

# Configurar buildozer.spec com keystore
# android.release_artifact = aab
# p4a ...

buildozer android release
# AAB em bin/
```

## Flutter Pro (Campeão - 6 semanas)

### Setup
```bash
# Instalar Flutter SDK https://flutter.dev
flutter --version

cd android_app/flutter_pro
flutter pub get
```

### Rodar
```bash
flutter run              # device ou emulator
flutter run -d chrome    # web (para testar)
```

### Build APK debug
```bash
flutter build apk --debug
# build/app/outputs/flutter-apk/app-debug.apk
```

### Build AAB release (Play Store)
```bash
# Criar keystore
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Criar android/key.properties
echo "storePassword=SUA_SENHA
keyPassword=SUA_SENHA
keyAlias=upload
storeFile=/home/user/upload-keystore.jks" > android/key.properties

# Build AAB
flutter build appbundle --release
# build/app/outputs/bundle/release/app-release.aab

# Build APK release
flutter build apk --release
```

### Firebase setup (opcional mas recomendado)
```bash
# Instalar Firebase CLI
npm install -g firebase-tools
firebase login
flutterfire configure --project=lotofacil-pro
# Gera lib/firebase_options.dart
```

## API Backend

### Local
```bash
cd android_app/api
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8000
uvicorn main_real:app --reload --port 8000 --env-file .env

# Docs
open http://localhost:8000/docs
```

### Deploy Cloud Run (recomendado)
```bash
# Dockerfile já pronto? Criar:
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main_real:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Deploy
gcloud run deploy lotofacil-api --source . --region us-central1 --allow-unauthenticated
```

## Play Store

### Checklist antes de upload
- [ ] AAB assinado com upload key
- [ ] targetSdk 34, minSdk 24
- [ ] Ícone 512x512, feature 1024x500, 5 screenshots
- [ ] Privacy Policy URL
- [ ] Data Safety preenchido
- [ ] Content rating
- [ ] Descrição curta/longa

### Upload
1. Play Console > Criar app > Lotofácil Pro
2. Configurar > Assinatura de app > Usar Play App Signing
3. Produção > Criar nova versão > Upload AAB
4. Preencher listing, content rating, data safety, pricing
5. Teste interno 20 testers 14 dias (obrigatório)
6. Depois closed testing, depois produção 20% rollout

## CI/CD com Fastlane (opcional)

```bash
# Instalar fastlane
gem install fastlane

cd android_app/flutter_pro/android
fastlane init

# fastlane supply para upload automático AAB
```

## Tamanho APK

- Flutter: ~35MB APK, ~20MB AAB (Play Store otimiza)
- Kivy: ~80MB APK com numpy, ~50MB sem pandas
- Dicas reduzir:
  - Remover torch/tensorflow do mobile
  - Usar --split-per-abi no Flutter
  - Proguard/R8 ativado
  - Remover assets não usados
