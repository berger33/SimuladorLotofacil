#!/bin/bash
# Otimiza imagens Play Store com TinyPNG / pngquant / jpegoptim
# Reduz ~16MB -> ~4-6MB sem perder qualidade

set -e

echo "🖼️ Otimizando imagens Play Store..."

SCREENSHOTS_DIR="../playstore/assets/screenshots"
PLAYSTORE_DIR="../playstore/assets"
FLUTTER_IMAGES_DIR="../flutter_pro/assets/images"

# Função otimiza com pngquant se disponível, senão avisa
optimize_png() {
    local file=$1
    if command -v pngquant &> /dev/null; then
        echo "  Otimizando $file com pngquant..."
        pngquant --quality=80-95 --skip-if-larger --ext .png --force "$file"
    elif command -v optipng &> /dev/null; then
        echo "  Otimizando $file com optipng..."
        optipng -o2 "$file"
    else
        echo "  ⚠️ pngquant/optipng não encontrado, pulando $file (instalar: sudo apt install pngquant optipng)"
    fi
}

# Verifica se tem API TinyPNG (melhor qualidade)
if [ -n "$TINYPNG_API_KEY" ]; then
    echo "🔑 TinyPNG API Key encontrada, usando API (melhor qualidade)"
    # Instala tinypng-cli se necessário
    if ! command -v tinypng &> /dev/null; then
        echo "📦 Instalando tinypng-cli..."
        npm install -g tinypng-cli || pip install tinypng-cli --break-system-packages
    fi
    
    echo "🗜️ Otimizando com TinyPNG..."
    for img in $SCREENSHOTS_DIR/*.png $PLAYSTORE_DIR/*.png $FLUTTER_IMAGES_DIR/*.png; do
        if [ -f "$img" ]; then
            echo "  TinyPNG: $img"
            tinypng "$img" || echo "  Falha TinyPNG para $img, tentando pngquant"
            optimize_png "$img"
        fi
    done
else
    echo "⚠️ TINYPNG_API_KEY não definida, usando pngquant/optipng local"
    echo "   Para melhor qualidade, criar conta https://tinypng.com/developers e export TINYPNG_API_KEY=xxx"
    echo ""
    
    for img in $SCREENSHOTS_DIR/*.png $PLAYSTORE_DIR/*.png $FLUTTER_IMAGES_DIR/*.png; do
        if [ -f "$img" ]; then
            optimize_png "$img"
        fi
    done
fi

# Mostra tamanhos antes/depois
echo ""
echo "📊 Tamanhos finais:"
du -h $SCREENSHOTS_DIR/*.png $PLAYSTORE_DIR/*.png $FLUTTER_IMAGES_DIR/*.png 2>/dev/null | sort -h

TOTAL=$(du -ch $SCREENSHOTS_DIR/*.png $PLAYSTORE_DIR/*.png 2>/dev/null | tail -1 | cut -f1)
echo ""
echo "✅ Total Play Store assets: $TOTAL"
echo "   (Original ~16MB, otimizado deve ser ~4-6MB)"
echo ""
echo "Próximos passos:"
echo "1. Verificar qualidade visual das imagens otimizadas"
echo "2. Upload no Play Console > Recursos gráficos"
echo "3. Se qualidade ruim, restaurar do git: git checkout -- android_app/playstore/assets/"
