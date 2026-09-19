# 🔨 Build AAB Real - Log e Instruções

## Tentativa Build no Ambiente Arena (2026-09-19)

### Ambiente
- Flutter: não instalado no container Arena (tentativa clone /tmp/flutter falhou SSL storage.googleapis.com)
- cwebp: não instalado, mas convertido via Python Pillow com sucesso
- Keystore: não existe, precisa gerar

### WebP Conversão - ✅ SUCESSO 94% economia

```bash
Original PNG: 16MB
- icon.png 1.9MB -> icon_512.webp 40KB (98% economia!)
- feature_graphic.png 2.4MB -> 135KB (94%)
- 01_dashboard.png 1475KB -> 82KB (94%)
- 02_gerador.png 1378KB -> 66KB (95%)
- 03_inteligencia.png 1607KB -> 78KB (95%)
- 04_ranking.png 1658KB -> 97KB (94%)
- 05_detalhes.png 1494KB -> 88KB (94%)
- 06_premium.png 1605KB -> 77KB (95%)
- 07_onboarding.png 1149KB -> 33KB (97%)
- 08_heatmap.png 2015KB -> 101KB (95%)
- 09_config.png 1242KB -> 57KB (95%)

Total WebP: 1012KB (1MB) vs PNG 16MB = 94% economia!
```

**Comando usado:**
```python
from PIL import Image
img = Image.open('icon.png')
img.save('icon_512.webp', 'WEBP', quality=85, method=6)
```

### Build AAB - Tentativa Flutter SDK

```bash
# Tentativa 1: Flutter não instalado
which flutter -> not found

# Tentativa 2: Clone Flutter stable
cd /tmp && git clone https://github.com/flutter/flutter.git -b stable --depth 1
# Clone OK 16074 arquivos

# Tentativa 3: flutter --version
/tmp/flutter/bin/flutter --version
# Falha: Downloading Dart SDK from storage.googleapis.com...
# curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL

# Causa: Rede Arena bloqueia storage.googleapis.com ou SSL issue
# Solução: Usar Docker ou build local
```

### Soluções para Build AAB Real 100%

#### Opção 1: Docker (Recomendado - 100% reproduzível)
```bash
cd android_app/flutter_pro
docker build -t lotofacil-build .
docker run --rm -v $(pwd)/build:/app/build lotofacil-build
# AAB em build/app/outputs/bundle/release/app-release.aab
```

#### Opção 2: Local com Flutter SDK
```bash
# Instalar Flutter https://flutter.dev/docs/get-started/install
flutter --version # deve ser 3.16+

cd android_app/flutter_pro
flutter pub get
flutter build appbundle --release
# AAB em build/app/outputs/bundle/release/app-release.aab ~20MB
```

#### Opção 3: GitHub Actions CI (Automático)
- Já configurado em `.github/workflows/ci.yml` lane build-flutter
- Adicionar secrets: KEYSTORE_BASE64, KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD
- Push na branch Aplicativo dispara build AAB automático
- Baixar artefato AAB em Actions > Artifacts

#### Opção 4: Fastlane (Deploy automático)
```bash
cd android_app/flutter_pro/android
fastlane internal  # build + upload teste interno
```

### Mock AAB para Teste Interno Play Console

Como não conseguimos build real no Arena por rede, criamos placeholder AAB para testar upload Play Console:

```bash
# Criar AAB mock vazio para testar processo Play Console (não instala, só testa upload)
mkdir -p /tmp/mock_aab
echo "Mock AAB Lotofácil Pro - substituir por AAB real do Flutter" > /tmp/mock_aab/README.txt
# Em produção, usar AAB real do Flutter ~20MB
```

**IMPORTANTE:** Para Play Store produção, SEMPRE usar AAB real do Flutter, não mock. Mock só serve para testar fluxo Play Console.

### Checklist Build AAB Real

- [ ] Flutter SDK 3.16+ instalado
- [ ] `flutter pub get` OK
- [ ] `flutter analyze` 0 erros
- [ ] Keystore gerado: `keytool -genkey -v -keystore ~/lotofacil-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload`
- [ ] `android/key.properties` preenchido com senhas reais (não commitar)
- [ ] `android/app/google-services.json` real do Firebase (ou .example para debug)
- [ ] `flutter build appbundle --release` gera `build/app/outputs/bundle/release/app-release.aab`
- [ ] Tamanho <150MB (Flutter ~20MB OK)
- [ ] Verificar targetSdk 34: `bundletool dump manifest --bundle=app-release.aab`
- [ ] Testar local: `bundletool build-apks --bundle=app-release.aab --output=app.apks && bundletool install-apks --apks=app.apks`

### Tamanho Esperado

- Flutter AAB release: ~20MB (Play Store otimiza para ~10MB download)
- Flutter APK release: ~35MB (ou ~15MB por ABI com --split-per-abi)
- Kivy APK: ~80MB com numpy

### Próximos Passos

1. Build local com Flutter SDK ou Docker
2. Otimizar imagens WebP já feito 94% economia
3. Upload AAB teste interno Play Console 20 testers 14 dias
4. Enquanto teste roda: deploy API Cloud Run + Firebase
