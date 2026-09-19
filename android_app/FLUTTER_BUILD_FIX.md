# 🔧 Flutter Build Fix - Solução Problemas Comuns

## Problema: flutter build appbundle falha

### 1. Keystore não encontrado
```
Keystore file not set for signing config release
```
**Solução:**
```bash
# Gerar keystore
keytool -genkey -v -keystore ~/lotofacil-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Criar key.properties
cat > android_app/flutter_pro/android/key.properties <<EOF
storePassword=SUA_SENHA
keyPassword=SUA_SENHA
keyAlias=upload
storeFile=/home/user/lotofacil-upload-keystore.jks
EOF
```

### 2. google-services.json faltando
```
File google-services.json is missing
```
**Solução:**
- Firebase Console > Baixar google-services.json
- Colocar em `android/app/google-services.json`
- Ou usar `.example` para build debug sem Firebase:
```bash
cp android/app/google-services.json.example android/app/google-services.json
```

### 3. AdMob App ID faltando
```
The Google Mobile Ads SDK was initialized incorrectly
```
**Solução:** Verificar `AndroidManifest.xml` tem:
```xml
<meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="ca-app-pub-...~..."/>
```

### 4. Versão Flutter incompatível
```
Pubspec.yaml flutter version mismatch
```
**Solução:**
```bash
flutter upgrade
flutter pub get
flutter clean
```

### 5. Dependências conflitantes
```
Version solving failed
```
**Solução:**
```bash
flutter pub upgrade --major-versions
flutter pub get
```

### 6. Build muito lento
**Solução:**
```bash
# Usar --no-tree-shake-icons para debug mais rápido
flutter build apk --debug --no-tree-shake-icons

# Para release, usar --split-per-abi para APKs menores por arquitetura
flutter build apk --release --split-per-abi
# Gera: app-armeabi-v7a-release.apk, app-arm64-v8a-release.apk, app-x86_64-release.apk
```

### 7. Tamanho AAB muito grande >150MB
**Causa:** torch, tensorflow, pandas incluídos
**Solução:** Já removido no core_shared, mas verificar pubspec não tem dependências pesadas. Flutter AAB deve ser ~20MB.

### 8. Erro NDK
```
NDK version mismatch
```
**Solução:** Em `android/app/build.gradle`:
```gradle
ndkVersion flutter.ndkVersion
```
E `local.properties`:
```
flutter.ndkVersion=25.1.8937393
```

---

## Build Debug vs Release

### Debug (para testar rápido)
```bash
flutter build apk --debug
# build/app/outputs/flutter-apk/app-debug.apk ~50MB
# Instala: flutter install ou adb install
```

### Release (para Play Store)
```bash
flutter build appbundle --release
# build/app/outputs/bundle/release/app-release.aab ~20MB
# Upload Play Console
```

### Profile (para testar performance)
```bash
flutter build apk --profile
```

---

## Testar AAB localmente com bundletool

```bash
# Baixar bundletool
wget https://github.com/google/bundletool/releases/download/1.15.6/bundletool-all-1.15.6.jar -O bundletool.jar

# Gerar APKS a partir de AAB
java -jar bundletool.jar build-apks --bundle=build/app/outputs/bundle/release/app-release.aab --output=app.apks --local-testing

# Instalar no device conectado
java -jar bundletool.jar install-apks --apks=app.apks

# Ou instalar APK específico
java -jar bundletool.jar install-apks --apks=app.apks --device-id=DEVICE_ID
```

---

## CI/CD GitHub Actions Build

Já configurado em `.github/workflows/ci.yml`:
- test-core
- test-api
- build-flutter (pub get + analyze)
- build-kivy (py_compile)

Para build AAB automático no CI, adicionar secrets no GitHub:
- `KEYSTORE_BASE64` - base64 do keystore
- `KEYSTORE_PASSWORD`
- `KEY_ALIAS`
- `KEY_PASSWORD`

E no workflow:
```yaml
- name: Decode keystore
  run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks

- name: Build AAB
  run: flutter build appbundle --release
```

---

## Verificar AAB antes de upload

```bash
# Listar conteúdo AAB
bundletool dump manifest --bundle=app-release.aab

# Verificar targetSdk
aapt dump badging app-release.aab | grep targetSdkVersion
# Deve ser 34

# Verificar permissões
aapt dump permissions app-release.aab
# Deve ter só INTERNET, ACCESS_NETWORK_STATE, BILLING, POST_NOTIFICATIONS
```

---

## Solução Definitiva: Build com Docker (evita problemas ambiente)

```dockerfile
FROM cirrusci/flutter:stable
WORKDIR /app
COPY . .
RUN flutter pub get
RUN flutter build appbundle --release
```

```bash
docker build -t lotofacil-build .
docker run --rm -v $(pwd)/build:/app/build lotofacil-build
```
