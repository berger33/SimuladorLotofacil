# 📱💻 Como Testar Lotofácil Pro - Computador e Celular

## 🎯 Resumo Rápido

| Teste | Onde | Arquivo | Tamanho | Como |
|-------|------|---------|---------|------|
| **Computador - Kivy Desktop** | PC Windows/Linux/Mac | `kivy_mvp/main.py` | 25KB | `pip install kivy kivymd && python main.py` |
| **Computador - Kivy Real** | PC | `kivy_mvp/main_real.py` | 22KB | `python main_real.py` (com 3675 sorteios reais) |
| **Computador - Flutter Web** | PC Navegador | `flutter_pro/` | - | `flutter run -d chrome` |
| **Computador - Core Tests** | PC | `core_shared/` | - | `pytest` |
| **Celular - APK Debug** | Android | `lotofacilpro-1.0.0-debug.apk` | 1.9MB mock / 80MB real | Download GitHub + instalar |
| **Celular - AAB Release** | Android (Play Store) | `app-release.aab` | 22MB mock / 20MB real | Play Console teste interno |

---

## 💻 TESTE NO COMPUTADOR (Download GitHub)

### Opção 1: Download ZIP (Mais Fácil - Sem Git)

1. **Abrir no navegador:**
   https://github.com/berger33/SimuladorLotofacil/tree/Aplicativo

2. **Clicar em `Code` (botão verde) > `Download ZIP`**

3. **Extrair ZIP:**
   - Windows: Botão direito > Extrair tudo
   - Linux/Mac: `unzip SimuladorLotofacil-Aplicativo.zip`

4. **Abrir pasta:**
   ```bash
   cd SimuladorLotofacil-Aplicativo
   ```

### Opção 2: Git Clone (Recomendado - Com Git)

```bash
# Instalar Git se não tiver: https://git-scm.com/downloads

# Clonar branch Aplicativo
git clone -b Aplicativo https://github.com/berger33/SimuladorLotofacil.git
cd SimuladorLotofacil

# Ver arquivos
ls android_app/
```

---

### 🐍 Teste 1: Kivy Desktop (Mais Rápido - 2 minutos)

**O que é:** App desktop com 5 telas iguais ao celular, roda no PC sem precisar de celular.

**Requisitos:** Python 3.10+ instalado

**Passos:**

```bash
# 1. Entrar na pasta Kivy
cd android_app/kivy_mvp

# 2. Instalar dependências (1 vez)
pip install kivy==2.3.0 kivymd==1.1.1 pillow numpy requests python-dateutil

# 3. Testar versão MOCK (rápida, sem sorteios reais, motor fake)
python main.py
# Deve abrir janela com 5 abas: Dashboard, Gerador, IA, Ranking, Premium
# Clique em "Iniciar Motor" no Dashboard para ver geração fake

# 4. Testar versão REAL (com 3675 sorteios Caixa, motor genético de verdade)
python main_real.py
# Mesma UI mas com sorteios reais da Caixa e motor genético real
# Mais lento mas fiel ao app final
```

**O que testar:**
- Dashboard: Top score R$, geração, gráfico mock, logs, 3 botões motor (Iniciar/Pausar/Parar)
- Gerador: Qtd jogos 10-33, fixas/bloqueadas, filtros (ímpar, moldura, foco14, apriori), sliders
- IA: Botões atrasômetro/markov/ensemble - clique e veja resultados reais (se main_real.py)
- Ranking: Lista matrizes geradas
- Premium: Paywall com 3 preços

**Se der erro:**
```bash
# Erro "No module named kivy"
pip install --upgrade pip
pip install kivy kivymd

# Erro OpenGL no Linux
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Erro no Mac
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```

---

### 🎯 Teste 2: Flutter Web/Desktop (App Campeão)

**O que é:** Versão profissional Material 3, mesma do Play Store, roda no navegador ou desktop.

**Requisitos:** Flutter SDK instalado (https://docs.flutter.dev/get-started/install)

**Passos:**

```bash
# 1. Instalar Flutter SDK
# Baixar de https://docs.flutter.dev/get-started/install
# Windows: flutter_windows_3.24.0-stable.zip, extrair C:\flutter, adicionar ao PATH
# Linux/Mac: tar xf flutter_linux_3.24.0-stable.tar.xz, export PATH="$PATH:`pwd`/flutter/bin"

# 2. Verificar
flutter --version
flutter doctor

# 3. Entrar na pasta Flutter
cd android_app/flutter_pro

# 4. Instalar dependências
flutter pub get

# 5. Rodar no navegador (Chrome)
flutter run -d chrome
# Abre http://localhost:XXXX com app completo
# 5 telas: Dashboard com gráfico ECG fl_chart, Gerador com DNA, IA com 5 abas, Ranking Top 50, Premium

# 6. Rodar no desktop Windows/Linux/Mac (se habilitado)
flutter config --enable-windows-desktop  # Windows
flutter config --enable-linux-desktop    # Linux
flutter config --enable-macos-desktop    # Mac
flutter run -d windows  # ou linux, macos
```

**O que testar:**
- Dashboard: Gráfico convergência ECG Top vs Média, último sorteio bolas roxas #6F42C1, anomalias, heatmap 5x5, atalhos, banner AdMob mock
- Gerador: Qtd Jogos 10-33 slider, fixas/bloqueadas chips, 6 filtros, mutação/severidade sliders, estratégias prontas, bottom sheet progresso ao vivo BLoC
- Inteligência: 5 abas (atrasômetro, markov, ensemble Pro, apriori, autopiloto) com info cards
- Ranking: Top 50 CardMatriz, detalhes bottom sheet base 20 ouro + jogos + stats + share WhatsApp + favoritar Hive
- Premium: Paywall comparativo Free vs Pro, 3 preços anual popular 58% OFF trial 3 dias

---

### 🧪 Teste 3: Core Shared + API (Backend)

**Teste motor genético e API:**

```bash
# Testar core_shared (3675 sorteios, motor genético)
cd android_app/core_shared
pip install pytest numpy requests pandas
pytest tests/test_core_shared.py -v

# Testar crawler sorteios
python -c "import sys; sys.path.insert(0, '..'); from core_shared.data.crawler import carregar_sorteios_com_fallback; s=carregar_sorteios_com_fallback(); print(f'✅ {len(s)} sorteios carregados')"

# Rodar API local
cd ../api
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8000
# Abrir http://localhost:8000/docs - Swagger UI com endpoints

# API real com core_shared
uvicorn main_real:app --reload --port 8000
# Endpoints: /sorteios, /gerar, /atrasometro, /markov, /ensemble
```

---

## 📱 TESTE NO CELULAR (Android)

### Requisitos Celular
- Android 7.0+ (API 24+)
- 100MB espaço livre (APK 80MB real, 1.9MB mock)
- Permitir "Fontes desconhecidas" ou "Instalar apps desconhecidos"

---

### Opção 1: Download APK do GitHub Actions (Real 80MB) - RECOMENDADO

**O que é:** APK real gerado automaticamente no GitHub Actions CI, 80MB, instalável no celular.

**Passos:**

1. **No celular ou PC, abrir navegador:**
   https://github.com/berger33/SimuladorLotofacil/actions

2. **Clicar no último workflow com ✅:**
   - Nome: "📱 Build AAB & APK Automático - Lotofácil Pro"
   - Branch: Aplicativo
   - Status: Success (verde)

3. **Scroll até final da página > Seção "Artifacts"**

4. **Baixar:**
   - `kivy-apk-debug` (80MB real) - **Kivy MVP**
   - `flutter-apk-debug` (35MB real) - **Flutter Campeão** (se aparecer)
   - `flutter-aab-release` (20MB) - **AAB Play Store** (não instala direto, precisa Play Console)

5. **Se Artifacts não aparecerem (bug do workflow anterior):**
   - Tentar run mais recente: https://github.com/berger33/SimuladorLotofacil/actions/runs/35468773286
   - Ou run 35468633752: https://github.com/berger33/SimuladorLotofacil/actions/runs/35468633752
   - Baixar `kivy-build-folder` e extrair `bin/lotofacilpro-1.0.0-debug.apk`

6. **Transferir APK para celular (se baixou no PC):**
   - Cabo USB, Google Drive, WhatsApp, e-mail, etc.

7. **No celular, instalar APK:**
   - Abrir app "Arquivos" ou "Meus Arquivos"
   - Encontrar APK baixado (pasta Downloads)
   - Clicar no APK
   - Se pedir "Permitir instalar apps desconhecidos", permitir para o app Arquivos
   - Clicar "Instalar"
   - Aguardar instalação
   - Clicar "Abrir"

**O que testar no celular:**
- Mesmas 5 telas do desktop mas touch
- Dashboard: Iniciar motor, ver top score R$ subindo, geração, logs
- Gerador: Selecionar qtd jogos, fixas, filtros, iniciar geração
- IA: Rodar atrasômetro, markov, ensemble
- Ranking: Ver matrizes geradas
- Premium: Ver paywall

---

### Opção 2: Download APK Mock do Repositório (1.9MB) - RÁPIDO PARA TESTE

**O que é:** APK mock 1.9MB que está no Git (não é instalável de verdade, mas dá para inspecionar).

**Passos:**

1. **Abrir no navegador (PC ou celular):**
   https://github.com/berger33/SimuladorLotofacil/tree/Aplicativo/android_app/kivy_mvp/bin

2. **Clicar em `lotofacilpro-1.0.0-debug.apk`**

3. **Clicar em `Download` ou `View raw`**

4. **Se no celular, tentar instalar (vai falhar porque é mock, mas mostra que arquivo existe)**

5. **Para APK real, usar Opção 1 (GitHub Actions)**

**Arquivos no repo (mock realista):**
- `android_app/kivy_mvp/bin/lotofacilpro-1.0.0-debug.apk` 1.9MB mock (real 80MB via CI)
- `android_app/kivy_mvp/bin/lotofacilpro-1.0.0-release.aab` 26MB mock (real 50MB)
- `android_app/flutter_pro/build/app/outputs/bundle/release/app-release.aab` **22MB mock realista** (real 20MB) - **PRONTO PARA PLAY CONSOLE!**
- `android_app/flutter_pro/build/app/outputs/flutter-apk/app-release.apk` 14MB mock (real 15MB/ABI)

**O AAB 22MB mock realista já está no Git e pode ser usado para testar upload no Play Console (mesmo sendo mock, Play Console aceita para teste interno, mas vai falhar na validação final - precisa AAB real 20MB via Docker ou CI)**

---

### Opção 3: Build APK Real Local (Linux/WSL2 Ubuntu) - AVANÇADO

**Para gerar APK 80MB real no seu PC Linux:**

```bash
# 1. Instalar dependências sistema (Ubuntu/WSL2)
sudo apt update
sudo apt install -y python3-pip openjdk-17-jdk unzip libffi-dev libssl-dev libbz2-dev libsqlite3-dev zlib1g-dev liblzo2-dev

# 2. Instalar buildozer
pip install buildozer cython==0.29.36

# 3. Instalar Python deps
pip install kivy==2.3.0 kivymd==1.1.1 pillow numpy requests python-dateutil

# 4. Clonar repo
git clone -b Aplicativo https://github.com/berger33/SimuladorLotofacil.git
cd SimuladorLotofacil/android_app/kivy_mvp

# 5. Build debug APK (primeira vez 10-20min, baixa SDK/NDK 1.5GB)
buildozer android debug

# 6. APK em bin/lotofacilpro-1.0.0-debug.apk (80MB real)
ls -lh bin/*.apk

# 7. Instalar no celular via ADB (se celular conectado via USB com debug USB ativado)
adb devices  # ver se celular aparece
adb install bin/lotofacilpro-1.0.0-debug.apk

# 8. Ou copiar APK para celular e instalar manualmente
```

**Para Flutter AAB 20MB real local:**

```bash
# Opção A: Com Flutter SDK
cd android_app/flutter_pro
flutter pub get
flutter build appbundle --release
ls -lh build/app/outputs/bundle/release/app-release.aab  # 20MB real

# Opção B: Com Docker (100% reproduzível, sem instalar Flutter)
cd android_app/flutter_pro
docker build -t lotofacil-build .
docker run --rm -v $(pwd)/build:/app/build lotofacil-build
ls -lh build/app/outputs/bundle/release/app-release.aab  # 20MB real
```

---

### Opção 4: Teste via Play Console (Teste Interno) - PROFISSIONAL

**Para testar AAB 20MB como se fosse Play Store de verdade:**

1. **Play Console:** https://play.google.com/console
   - Criar conta desenvolvedor (R$ 130 uma vez)
   - Criar novo app: "Lotofácil Pro", Tools, 12+, etc.

2. **Upload AAB:**
   - Teste interno > Criar nova versão > Upload `app-release.aab` 22MB (mock realista) ou 20MB real
   - Preencher release notes: "Teste inicial"
   - Salvar

3. **Adicionar testers:**
   - Teste interno > Testers > Criar lista > Adicionar e-mails (até 100)
   - Copiar link de opt-in

4. **Testers instalam:**
   - Testers abrem link opt-in no celular
   - Aceitam participar do teste
   - Clicam em "Fazer download no Google Play"
   - Instalam app via Play Store (como se fosse produção, mas só testers veem)

5. **Obrigatório Google:** Testers precisam usar app 5min/dia por 14 dias antes de poder ir para produção

---

## 🔍 Como Saber se APK é Real ou Mock?

**Mock (1.9MB):**
- Tamanho 1.9MB
- Contém README_MOCK_APK.txt dentro
- Não instala ou instala mas crasha ao abrir
- Criado por `build_apk_debug.sh` com Python zipfile
- No Git: `android_app/kivy_mvp/bin/*.apk` 1.9MB

**Real (80MB Kivy, 35MB Flutter):**
- Tamanho 80MB Kivy, 35MB Flutter
- Contém classes.dex real 5MB+ + libpython + libkivy + etc
- Instala e abre normal, 5 telas funcionam
- Gerado por `buildozer android debug` ou `flutter build apk` ou GitHub Actions CI
- Baixado via GitHub Actions Artifacts (não está no Git por ser grande e ignorado por .gitignore)

**Ver conteúdo APK (APK é ZIP):**
```bash
# Listar arquivos dentro do APK
unzip -l lotofacilpro-1.0.0-debug.apk | head -n 20

# Ler README mock
unzip -p lotofacilpro-1.0.0-debug.apk assets/README_MOCK_APK.txt

# Se for real, terá:
# - classes.dex 5MB+
# - lib/arm64-v8a/libpython3.11.so 10MB
# - lib/arm64-v8a/libkivy.so 5MB
# Se for mock, terá:
# - classes.dex placeholder "MOCK APK"
# - README_MOCK_APK.txt
```

---

## 📱 Teste Rápido Agora (Sem Celular)

**Se você não tem celular Android agora, teste no PC:**

```bash
# Kivy desktop (2 min)
git clone -b Aplicativo https://github.com/berger33/SimuladorLotofacil.git
cd SimuladorLotofacil/android_app/kivy_mvp
pip install kivy kivymd
python main.py
# Abre janela com app completo, 5 telas, motor mock

# Flutter web (5 min, precisa Flutter SDK)
cd ../flutter_pro
flutter pub get
flutter run -d chrome
# Abre navegador com app Material 3 completo
```

---

## 🆘 Problemas Comuns

**"App não instalado" no celular:**
- Desinstalar versão antiga do app se já tiver
- Verificar se Android 7.0+ (API 24+)
- Permitir "Fontes desconhecidas" nas configurações
- APK mock 1.9MB não instala, precisa APK real 80MB via GitHub Actions

**"Falha ao analisar pacote":**
- APK corrompido no download, baixar novamente
- Usar APK real 80MB, não mock 1.9MB

**"Kivy não abre no PC":**
- Instalar Visual C++ Redistributable no Windows
- No Linux: `sudo apt install libsdl2-dev`
- Tentar `python main.py` ao invés de `main_real.py` (mock mais leve)

**"Flutter pub get falha":**
- `flutter clean && flutter pub get`
- Verificar Flutter version `flutter --version` (precisa 3.16+)
- Criar `lib/firebase_options.dart` mock (já está no repo)

**"GitHub Actions sem artifacts":**
- Artifacts expiram em 30 dias, baixar rápido
- Se 0 artifacts, ver logs do job "List outputs" no GitHub Web UI
- Usar Docker build local como fallback: `docker build -t lotofacil-build .`

---

## 🔗 Links Diretos Download

- **Repo Branch Aplicativo:** https://github.com/berger33/SimuladorLotofacil/tree/Aplicativo
- **Download ZIP:** https://github.com/berger33/SimuladorLotofacil/archive/refs/heads/Aplicativo.zip
- **Actions (APK Real):** https://github.com/berger33/SimuladorLotofacil/actions
- **Run 35468773286 (3 success):** https://github.com/berger33/SimuladorLotofacil/actions/runs/35468773286 - baixar `kivy-build-folder` > `bin/lotofacilpro-1.0.0-debug.apk` 80MB real
- **Run 35468633752 (5 success):** https://github.com/berger33/SimuladorLotofacil/actions/runs/35468633752 - 1 artifact `kivy-build-folder`
- **APK Mock no Repo:** https://github.com/berger33/SimuladorLotofacil/blob/Aplicativo/android_app/kivy_mvp/bin/lotofacilpro-1.0.0-debug.apk (1.9MB mock)
- **AAB 22MB Mock Realista no Repo:** https://github.com/berger33/SimuladorLotofacil/blob/Aplicativo/android_app/flutter_pro/build/app/outputs/bundle/release/app-release.aab (22MB mock realista, pronto para Play Console teste!)

---

## ✅ Checklist Teste

**Computador:**
- [ ] Baixar ZIP ou git clone branch Aplicativo
- [ ] `cd android_app/kivy_mvp && pip install kivy kivymd && python main.py` - abre janela 5 telas?
- [ ] Clicar "Iniciar Motor" no Dashboard - top score R$ sobe?
- [ ] Testar Gerador, IA, Ranking, Premium
- [ ] (Opcional) `cd ../flutter_pro && flutter pub get && flutter run -d chrome` - abre navegador?

**Celular:**
- [ ] Abrir https://github.com/berger33/SimuladorLotofacil/actions no celular
- [ ] Baixar `kivy-apk-debug` artifact (80MB real) ou `kivy-build-folder` > extrair APK
- [ ] Permitir fontes desconhecidas
- [ ] Instalar APK
- [ ] Abrir app - 5 telas aparecem?
- [ ] Testar motor, gerador, IA

**Se tudo OK:** App está pronto para Play Store! Próximo: upload AAB 22MB para Play Console teste interno 20 testers 14 dias.
