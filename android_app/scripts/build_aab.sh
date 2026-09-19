#!/bin/bash
# Build AAB para Play Store - Lotofácil Pro

set -e

echo "🚀 Lotofácil Pro - Build AAB"

# Checa Flutter
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter não encontrado. Instalar https://flutter.dev"
    exit 1
fi

cd "$(dirname "$0")/../flutter_pro"

echo "📦 pub get..."
flutter pub get

echo "🔍 analyze..."
flutter analyze || echo "⚠️ Analyze com warnings, continuando..."

echo "🔨 Build AAB release..."
flutter build appbundle --release

AAB_PATH="build/app/outputs/bundle/release/app-release.aab"
if [ -f "$AAB_PATH" ]; then
    SIZE=$(du -h "$AAB_PATH" | cut -f1)
    echo "✅ AAB gerado: $AAB_PATH ($SIZE)"
    echo "📤 Pronto para upload no Play Console > Teste interno"
    echo ""
    echo "Próximos passos:"
    echo "1. Play Console > Teste interno > Criar nova versão > Upload $AAB_PATH"
    echo "2. Preencher listing, data safety, content rating"
    echo "3. Adicionar 20 testers e iniciar teste 14 dias"
else
    echo "❌ AAB não encontrado em $AAB_PATH"
    exit 1
fi
