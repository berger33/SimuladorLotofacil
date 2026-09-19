#!/bin/bash
# 🚀 PUBLISH 1-CLIQUE - Lotofácil Pro Play Store
# Faz tudo: otimiza imagens -> build AAB -> verifica -> instruções Play Console
# Uso: ./scripts/publish_1click.sh

set -e

echo "🚀 Lotofácil Pro - PUBLISH 1-CLIQUE"
echo "===================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Checa diretório
if [ ! -d "flutter_pro" ]; then
    echo -e "${RED}❌ Rodar dentro de android_app/: cd android_app && ./scripts/publish_1click.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Checklist pré-build:${NC}"

# 1. Flutter instalado?
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}❌ Flutter não encontrado. Instalar https://flutter.dev${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Flutter: $(flutter --version | head -n1)${NC}"
fi

# 2. Keystore existe?
if [ ! -f "$HOME/lotofacil-upload-keystore.jks" ] && [ ! -f "flutter_pro/android/upload-keystore.jks" ]; then
    echo -e "${YELLOW}⚠️ Keystore não encontrado. Gerar? (s/n)${NC}"
    read -r resp
    if [[ "$resp" == "s" ]]; then
        echo "🔑 Gerando keystore..."
        keytool -genkey -v -keystore ~/lotofacil-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
        echo -e "${GREEN}✅ Keystore gerado em ~/lotofacil-upload-keystore.jks - GUARDAR EM LOCAL SEGURO + 1Password!${NC}"
    else
        echo -e "${RED}❌ Keystore necessário para AAB release. Abortando.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Keystore encontrado${NC}"
fi

# 3. key.properties existe?
if [ ! -f "flutter_pro/android/key.properties" ]; then
    echo -e "${YELLOW}⚠️ key.properties não encontrado. Criar a partir de example? (s/n)${NC}"
    read -r resp
    if [[ "$resp" == "s" ]]; then
        cp flutter_pro/android/keystore.properties.example flutter_pro/android/key.properties
        echo -e "${YELLOW}📝 Editar flutter_pro/android/key.properties com senhas reais${NC}"
        echo "   Pressione Enter após editar..."
        read -r
    else
        echo -e "${RED}❌ key.properties necessário. Abortando.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ key.properties encontrado${NC}"
fi

# 4. google-services.json existe?
if [ ! -f "flutter_pro/android/app/google-services.json" ]; then
    echo -e "${YELLOW}⚠️ google-services.json não encontrado. Usar example para build debug? (s/n)${NC}"
    read -r resp
    if [[ "$resp" == "s" ]]; then
        cp flutter_pro/android/app/google-services.json.example flutter_pro/android/app/google-services.json
        echo -e "${YELLOW}⚠️ Usando google-services.json.example - Firebase não funcionará, mas build OK para teste${NC}"
    else
        echo -e "${YELLOW}⚠️ Continuando sem Firebase (Analytics/Crashlytics desabilitados)${NC}"
    fi
else
    echo -e "${GREEN}✅ google-services.json encontrado${NC}"
fi

echo ""
echo -e "${YELLOW}🖼️ Passo 1: Otimizando imagens...${NC}"
if [ -f "scripts/optimize_images.sh" ]; then
    chmod +x scripts/optimize_images.sh
    ./scripts/optimize_images.sh || echo -e "${YELLOW}⚠️ Otimização falhou ou pngquant não instalado, continuando...${NC}"
else
    echo -e "${YELLOW}⚠️ optimize_images.sh não encontrado, pulando${NC}"
fi

echo ""
echo -e "${YELLOW}📦 Passo 2: Flutter pub get + analyze...${NC}"
cd flutter_pro
flutter pub get
flutter analyze || echo -e "${YELLOW}⚠️ Analyze com warnings, continuando...${NC}"

echo ""
echo -e "${YELLOW}🔨 Passo 3: Build AAB release...${NC}"
flutter build appbundle --release

AAB_PATH="build/app/outputs/bundle/release/app-release.aab"
if [ -f "$AAB_PATH" ]; then
    SIZE=$(du -h "$AAB_PATH" | cut -f1)
    echo -e "${GREEN}✅ AAB gerado: $AAB_PATH ($SIZE)${NC}"
    
    # Verifica tamanho
    SIZE_BYTES=$(stat -c%s "$AAB_PATH" 2>/dev/null || stat -f%z "$AAB_PATH" 2>/dev/null || echo 0)
    if [ "$SIZE_BYTES" -gt 157286400 ]; then # 150MB
        echo -e "${RED}❌ AAB muito grande >150MB ($SIZE). Verificar dependências.${NC}"
        exit 1
    fi
    
    # Verifica targetSdk com aapt se disponível
    if command -v aapt &> /dev/null; then
        echo "🔍 Verificando targetSdk..."
        aapt dump badging "$AAB_PATH" | grep targetSdkVersion || echo "⚠️ aapt não conseguiu ler targetSdk"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 BUILD CONCLUÍDO COM SUCESSO!${NC}"
    echo "===================================="
    echo -e "📦 AAB: ${GREEN}$AAB_PATH ($SIZE)${NC}"
    echo -e "📊 Tamanho: ${GREEN}$SIZE (limite Play Store 150MB base, 2GB com expansion)${NC}"
    echo ""
    echo -e "${YELLOW}📤 Próximos passos MANUAIS (fora do script):${NC}"
    echo ""
    echo "1. GitHub Pages Privacy (2 min):"
    echo "   GitHub > berger33/SimuladorLotofacil > Settings > Pages > Source: Deploy from branch > Branch: Aplicativo / docs > Save"
    echo "   Testar: https://berger33.github.io/SimuladorLotofacil/privacy.html"
    echo ""
    echo "2. Play Console (15 min):"
    echo "   https://play.google.com/console > Criar app > Lotofácil Pro - IA & Estatística"
    echo "   - Categoria: Ferramentas"
    echo "   - Privacy URL: https://berger33.github.io/SimuladorLotofacil/privacy.html"
    echo "   - Data Safety, Content Rating 12+, Público 18+, 20 testers"
    echo "   - Produtos IAP: monthly R\$19,90 yearly R\$99 trial 3d lifetime R\$199"
    echo "   - Recursos gráficos: Upload icon_512.png, feature_graphic.png, 9 screenshots"
    echo ""
    echo "3. Upload AAB Teste Interno:"
    echo "   Teste interno > Criar nova versão > Upload $AAB_PATH"
    echo "   Notas: Primeira versão com IA completa, 3675 sorteios, motor genético, 5 telas Material 3"
    echo "   Salvar > Revisar > Iniciar lançamento teste interno"
    echo "   Enviar link teste para 20 emails e pedir uso 5 min/dia por 14 dias (obrigatório Google)"
    echo ""
    echo "4. Enquanto teste interno roda 14 dias (paralelo):"
    echo "   - Deploy API: cd android_app/api && gcloud run deploy lotofacil-api --source . --region us-central1 --allow-unauthenticated"
    echo "   - Firebase: Console > Criar projeto lotofacil-pro > Adicionar Android app"
    echo "   - AdMob: Criar App ID produção, trocar IDs teste por produção"
    echo "   - Integrar BannerAdWidget + IAPService UI"
    echo ""
    echo "5. Após 14 dias teste interno OK:"
    echo "   Promover: internal -> closed (100 testers) -> open (500) -> production 20% -> 50% -> 100%"
    echo "   Com Fastlane: cd flutter_pro/android && fastlane internal / production_20"
    echo ""
    echo -e "${GREEN}📚 Guias completos:${NC}"
    echo "   - RELEASE_CHECKLIST_1CLICK.md"
    echo "   - PROXIMOS_PASSOS_PLAYSTORE.md"
    echo "   - FIREBASE_ADMOB_SETUP.md"
    echo "   - BUILD_GUIDE.md"
    echo ""
    echo -e "${GREEN}🎯 Tempo até produção: 16 dias (2 dias build + 14 dias teste obrigatório)${NC}"
    echo -e "${GREEN}💰 Receita potencial Mês 1: 10k instalações ~R\$10k${NC}"
    
    cd ..
else
    echo -e "${RED}❌ AAB não encontrado em $AAB_PATH${NC}"
    exit 1
fi
