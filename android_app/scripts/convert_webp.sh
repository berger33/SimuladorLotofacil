#!/bin/bash
# Converte PNG para WebP para Play Store (menor tamanho, mesma qualidade)
# WebP é aceito na Play Store e reduz ~30% tamanho

set -e

echo "🖼️ Convertendo PNG para WebP (Play Store aceita, ~30% menor)..."

PLAYSTORE_DIR="../playstore/assets"
SCREENSHOTS_DIR="../playstore/assets/screenshots"
FLUTTER_IMAGES_DIR="../flutter_pro/assets/images"

# Checa cwebp
if ! command -v cwebp &> /dev/null; then
    echo "⚠️ cwebp não encontrado. Instalar:"
    echo "  Ubuntu: sudo apt install webp"
    echo "  Mac: brew install webp"
    echo "  Ou continuar com PNG (Play Store aceita PNG também)"
    echo ""
    echo "Continuar com PNG? (s/n)"
    read -r resp
    if [[ "$resp" != "s" ]]; then
        exit 1
    fi
    echo "✅ Usando PNG original (OK para Play Store)"
    exit 0
fi

convert_to_webp() {
    local png_file=$1
    local webp_file="${png_file%.png}.webp"
    
    if [ -f "$png_file" ]; then
        echo "  Convertendo $png_file -> $webp_file"
        cwebp -q 85 "$png_file" -o "$webp_file"
        local png_size=$(stat -c%s "$png_file" 2>/dev/null || stat -f%z "$png_file" 2>/dev/null || echo 0)
        local webp_size=$(stat -c%s "$webp_file" 2>/dev/null || stat -f%z "$webp_file" 2>/dev/null || echo 0)
        if [ "$png_size" -gt 0 ] && [ "$webp_size" -gt 0 ]; then
            local saved=$((100 - webp_size * 100 / png_size))
            echo "    ${png_size} -> ${webp_size} bytes (economia ${saved}%)"
        fi
    fi
}

echo "📸 Convertendo screenshots..."
for png in $SCREENSHOTS_DIR/*.png; do
    if [ -f "$png" ]; then
        convert_to_webp "$png"
    fi
done

echo ""
echo "🎨 Convertendo feature graphic e icon..."
for png in $PLAYSTORE_DIR/*.png $FLUTTER_IMAGES_DIR/*.png; do
    if [ -f "$png" ]; then
        # Não converter ícone adaptativo que precisa ser PNG
        if [[ "$png" != *"foreground"* && "$png" != *"background"* ]]; then
            convert_to_webp "$png"
        fi
    fi
done

echo ""
echo "📊 Tamanhos finais WebP:"
du -h $SCREENSHOTS_DIR/*.webp $PLAYSTORE_DIR/*.webp 2>/dev/null | sort -h || echo "Nenhum WebP gerado"

TOTAL_PNG=$(du -ch $SCREENSHOTS_DIR/*.png $PLAYSTORE_DIR/*.png 2>/dev/null | tail -1 | cut -f1 || echo "N/A")
TOTAL_WEBP=$(du -ch $SCREENSHOTS_DIR/*.webp $PLAYSTORE_DIR/*.webp 2>/dev/null | tail -1 | cut -f1 || echo "N/A")

echo ""
echo "✅ PNG total: $TOTAL_PNG"
echo "✅ WebP total: $TOTAL_WEBP"
echo ""
echo "Play Store aceita PNG e WebP. WebP é ~30% menor, upload mais rápido."
echo "Você pode fazer upload de ambos, Play Store escolhe melhor."
